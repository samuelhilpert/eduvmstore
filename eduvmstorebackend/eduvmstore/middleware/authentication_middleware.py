import logging
import requests
from django.utils.timezone import now
from django.http import JsonResponse
from eduvmstore.db.models import Users, Roles
from eduvmstore.db.operations.roles import get_role_by_name

logger = logging.getLogger(__name__)

class KeystoneAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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

        request.user = user
        response = self.get_response(request)
        return response

    def validate_token_with_keystone(self, token):
        keystone_url = "http://localhost:3000/auth/tokens"
        headers = {'X-Auth-Token': token}
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
        user_id = keystone_user_info['id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            role = get_role_by_name("User")
            user = Users.objects.create(id=user_id, role_id=role)
        return user

    def check_user_access(self, request, user):
        required_access_level = self.get_required_access_level(request.path)
        return user.role_id.access_level >= required_access_level

    def get_required_access_level(self, path):
        return 3000