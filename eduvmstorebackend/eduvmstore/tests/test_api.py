import logging
from rest_framework.test import APITestCase
from django.urls import reverse

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes, Favorites
from eduvmstore.db.models import (AppTemplates, Users, Roles, AppTemplateInstantiationAttributes,
                                  AppTemplateAccountAttributes)
from unittest.mock import patch
import uuid

logger = logging.getLogger('eduvmstore_logger')

class AppTemplateViewSetTests(APITestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def create_app_template(self):
        return AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="API Test Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            creator_id=self.user,
            public=True,
            approved=False,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )

    def get_auth_headers(self, token="valid_token"):
        return {'HTTP_X_AUTH_TOKEN': token}

    def setUp(self):
        self.user = self.create_user_and_role()
        self.client.force_authenticate(user=self.user)
        self.app_template = self.create_app_template()

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_creates_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-list')
        name = "Test Create Template"
        data = {
            "image_id": str(uuid.uuid4()),
            "name": name,
            "description": "A test template",
            "short_description": "Test",
            "instantiation_notice": "Notice",
            "script": "Script",
            "instantiation_attributes": [
                {"name": "JavaVersion"},
                {"name": "InstallSpringboot"}
            ],
            "account_attributes": [
                {"name": "Username"},
                {"name": "Password"}
            ],
            "fixed_ram_gb": 1.0,
            "fixed_disk_gb": 10.0,
            "fixed_cores": 1.0,
            "per_user_ram_gb": 0.5,
            "per_user_disk_gb": 5.0,
            "per_user_cores": 0.5
        }
        response = self.client.post(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_updates_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-detail', args=[self.app_template.id])
        name = "API Updated Template"
        updated_instantiation_attributes_name = "Updated JavaVersion Field"
        data = {
            "name": name,
            "description": "An updated template",
            "short_description": "Updated",
            "instantiation_notice": "Updated Notice",
            "script": "Updated Script",
            "instantiation_attributes": [
                {"name": updated_instantiation_attributes_name},
                {"name": "SpringbootVersion"}
            ],
            "account_attributes": [
                {"name": "Username"},
                {"name": "Password"}
            ],
            "image_id": self.app_template.image_id,
            "approved": True,
            "fixed_ram_gb": 2.0,
            "fixed_disk_gb": 20.0,
            "fixed_cores": 2.0,
            "per_user_ram_gb": 1.0,
            "per_user_disk_gb": 10.0,
            "per_user_cores": 1.0
        }
        response = self.client.put(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], name)
        self.assertEqual(response.data["instantiation_attributes"][0]["name"],
                         updated_instantiation_attributes_name)
        self.assertEqual(response.data["approved"], False)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_filters_app_templates_by_search(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-list') + '?search=API'
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.app_template.name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collisions(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-check-name-collisions', kwargs={'name': self.app_template.name})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['collisions'])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collisions_no_collision(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-check-name-collisions', kwargs={'name': 'No Collision Template'})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['collisions'])

    # As soft delete is currently not used the assert statements are commented out
    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_soft_deletes_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        #instantiation_attribute = AppTemplateInstantiationAttributes.objects.create(
        #    app_template_id=self.app_template,
        #    name="JavaVersion"
        #)

        url = reverse('app-template-detail', args=[self.app_template.id])
        response = self.client.delete(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 204)
        #self.app_template.refresh_from_db()

        #self.assertTrue(self.app_template.deleted)
        #self.assertIsNotNone(self.app_template.deleted_at)
        #instantiation_attribute.refresh_from_db()
        #self.assertIsNotNone(instantiation_attribute.name)

class FavoritesViewSetTests(APITestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def create_app_template(self):
        app_template = AppTemplates.objects.create(
            id=uuid.uuid4(),
            image_id=uuid.uuid4(),
            name="Favorite Template",
            description="A favorite template",
            short_description="Favorite",
            instantiation_notice="Notice",
            script="Script",
            creator_id=self.user,
            public=True,
            approved=False,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        return app_template

    def get_auth_headers(self, token="valid_token"):
        return {'HTTP_X_AUTH_TOKEN': token}

    def setUp(self):
        self.user = self.create_user_and_role()
        self.client.force_authenticate(user=self.user)
        self.app_template = self.create_app_template()

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_adds_app_template_to_favorites(self, mock_validate_token):
         mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
         url = reverse('favorite-list')
         data = {"app_template_id": self.app_template.id}
         response = self.client.post(url, data, format='json', **self.get_auth_headers())
         self.assertEqual(response.status_code, 201)
         self.assertTrue(1, Favorites.objects.all().count())

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_removes_app_template_from_favorites(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.user.id, 'name': 'Admin'}

        Favorites.objects.create(id=uuid.uuid4(), app_template_id=self.app_template, user_id=self.user)

        url = reverse('favorite-delete-by-app-template')
        data = {"app_template_id": self.app_template.id}
        response = self.client.delete(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Favorites.objects.filter(
            app_template_id=self.app_template.id, user_id=self.user.id).exists())

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_lists_favorites_for_user(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.user.id, 'name': 'Admin'}
        Favorites.objects.create(app_template_id=self.app_template, user_id=self.user)
        url = reverse('app-template-favorites')
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.app_template.name)