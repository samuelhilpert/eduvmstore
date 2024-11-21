import logging
import requests
from django.utils.timezone import now
from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings

from eduvmstore.db.models import Users
from eduvmstore.db.operations.roles import get_role_by_name
from eduvmstore.db.operations.users import get_user_by_id, create_user
from eduvmstore.config.access_levels import REQUIRED_ACCESS_LEVELS

logger = logging.getLogger(__name__)

class KeystoneAuthenticationMiddleware:
    """
    Middleware for Keystone authentication and user access control.

    This middleware handles token validation with Keystone, user retrieval or creation,
    if none exists, and access level checking based on request routing.

    :param function get_response: Callable that processes the request after middleware execution
    """
    def __init__(self, get_response):
        """
        Initialize the middleware with a get_response callable.

        :param function get_response: Callable that processes the request after middleware execution
        """
        self.get_response = get_response

    def __call__(self, request):
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
        if not self.check_user_access(request, user):
            logger.error('Access denied for user: %s', user.id)
            return JsonResponse({'error': 'Access denied'}, status=403)

        request.myuser = user
        response = self.get_response(request)
        return response

    def validate_token_with_keystone(self, token):
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

    def get_or_create_user(self, keystone_user_info):
        """
        Retrieve or create a user based on Keystone user information.

        :param dict keystone_user_info: Keystone user information dictionary
        :return: User instance
        :rtype: Users
        """
        user_id = keystone_user_info['id']
        try:
            user = get_user_by_id(user_id)
            if user is None:
                raise Users.DoesNotExist
        except Users.DoesNotExist:
            role = get_role_by_name("User")
            user_data = {
                'id': user_id,
                'role_id': role
            }
            user = create_user(user_data)
        return user

    def check_user_access(self, request, user):
        """
        Check if the user has sufficient access level for the requested route.

        :param HttpRequest request: The HTTP request object
        :param Users user: The user instance to check access for
        :return: True if access is allowed, False otherwise
        :rtype: bool
        """
        required_access_level = self.get_required_access_level(request)
        return user.role_id.access_level >= required_access_level

    def get_required_access_level(self, request):
        """
        Determine the required access level for a specific request route.

        :param HttpRequest request: The HTTP request object
        :return: Required access level for the route
        :rtype: int
        """
        resolver_match = resolve(request.path)
        method = request.method
        route_name = resolver_match.route

        # Map generated routes of the default router to expected routes
        route_mapping = {
            'app-template-list': 'GET /app-templates',
            'app-template-detail': 'GET /app-templates/{id}',
            'app-template-create': 'POST /app-templates',
            'app-template-update': 'PUT /app-templates/{id}',
            'app-template-partial-update': 'PATCH /app-templates/{id}',
            'app-template-destroy': 'DELETE /app-templates/{id}',
            'app-template-check-name-collisions': 'GET /app-templates/name/{name}/collisions',
            'user-list': 'GET /users',
            'user-detail': 'GET /users/{id}',
            'user-change-role': 'PATCH /users/{id}/role',
            'user-destroy': 'DELETE /users/{id}',
            'image-list': 'GET /images',
            'image-detail': 'GET /images/{id}',
            'flavor-selection': 'POST /flavors/selection',
            'instance-creation': 'POST /instances/launch',
        }

        endpoint = route_mapping.get(route_name, f"{method} {resolver_match.route}")
        return REQUIRED_ACCESS_LEVELS.get(endpoint, 1000)  # Default to 1000 if not found
