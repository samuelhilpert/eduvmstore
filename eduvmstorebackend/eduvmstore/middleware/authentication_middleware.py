import logging
import requests

from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from eduvmstore.db.models import Users
from eduvmstore.db.operations.users import get_user_by_id, create_user
from eduvmstore.config.access_levels import REQUIRED_ACCESS_LEVELS, DEFAULT_ACCESS_LEVEL
from eduvmstore.utils.access_control import check_request_access

logger = logging.getLogger('eduvmstore_logger')

class KeystoneAuthenticationMiddleware:
    """
    Middleware for Keystone authentication and user access control.

    This middleware handles token validation with Keystone, user retrieval or creation,
    if none exists, and access level checking based on request routing.

    :param function get_response: Callable that processes the request after middleware execution
    """
    def __init__(self, get_response) -> None:
        """
        Initialize the middleware with a get_response callable.

        :param function get_response: Callable that processes the request after middleware execution
        """
        self.get_response = get_response

    def __call__(self, request) -> JsonResponse:
        """
        Process the request to validate the authentication token and user access.

        :param HttpRequest request: The incoming HTTP request
        :return: JsonResponse or the response from the view function
        :rtype: JsonResponse or HttpResponse
        """
        token = request.headers.get('X-Auth-Token')
        if not token:
            logger.error('OpenStack Authentication Token missing')
            return JsonResponse({'error': 'OpenStack Authentication Token missing'}, status=401)

        keystone_user_info = self.validate_token_with_keystone(token)
        if keystone_user_info is None:
            logger.error('Invalid token')
            return JsonResponse({'error': 'Invalid token'}, status=401)

        user = self.get_or_create_user(keystone_user_info)
        request.myuser = user
        if not check_request_access(request):
            logger.error('Access denied for user: %s', user.id)
            return JsonResponse({'error': f'Access level of user {user.id} not sufficient'}, status=403)

        response = self.get_response(request)
        return response

    def validate_token_with_keystone(self, token) -> dict or None:
        """
        Validate the OpenStack authentication token with Keystone.

        :param str token: The OpenStack token to validate
        :return: Dictionary with Keystone user information if valid, else None
        :rtype: dict or None
        """
        keystone_url = f"http://{settings.OPENSTACK['auth_url']}v3/auth/tokens"
        headers = {'X-Auth-Token': token, 'X-Subject-Token': token}
        try:
            response = requests.get(keystone_url, headers=headers)
            if response.status_code == 200:
                return response.json()['token']['user']
            else:
                logger.error('Keystone token validation failed with status code: %s', response.status_code)
                return None
        except requests.RequestException as e:
            logger.error('Keystone token validation request failed: %s', e)
            return None

    def get_or_create_user(self, keystone_user_info) -> Users:
        """
        Retrieve or create a user based on Keystone user information.

        :param dict keystone_user_info: Keystone user information dictionary
        :return: User instance
        :rtype: Users
        """
        user_id = keystone_user_info['id']
        keystone_role = keystone_user_info['name']

        try:
            user = get_user_by_id(user_id)
        except ObjectDoesNotExist:
            user_dict = {
                'id': user_id,
                'keystone_role_name': keystone_role
            }
            user =  create_user(user_dict)
        return user
