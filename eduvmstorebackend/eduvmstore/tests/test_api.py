import logging

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import (AppTemplates, Users, Roles, AppTemplateInstantiationAttributes,
                                  AppTemplateAccountAttributes, Favorites, AppTemplateSecurityGroups)
from unittest.mock import patch
import uuid

logger = logging.getLogger('eduvmstore_logger')


class AppTemplateViewSetTests(APITestCase):

    def create_user_and_role(self):
        admin_role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                          access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get(
                                              "access_level"))
        user_role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreUser").get("name"),
                                         access_level=DEFAULT_ROLES.get("EduVMStoreUser").get("access_level"))
        admin_user = Users.objects.create(role_id=admin_role)
        normal_user = Users.objects.create(role_id=user_role)
        self.admin_user = admin_user
        self.normal_user = normal_user

    def create_app_template(self):
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="API Test Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            ssh_user_requested=True,
            creator_id=self.admin_user,
            public=True,
            approved=False,
            volume_size_gb=100,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )
        AppTemplateInstantiationAttributes.objects.create(
            app_template_id=app_template,
            name="JavaVersion"
        )
        AppTemplateAccountAttributes.objects.create(
            app_template_id=app_template,
            name="Username"
        )
        AppTemplateSecurityGroups.objects.create(
            app_template_id=app_template,
            name="default"
        )
        return app_template

    def get_auth_headers(self, token="valid_token"):
        return {'HTTP_X_AUTH_TOKEN': token}

    def setUp(self):
        self.create_user_and_role()
        self.client.force_authenticate(user=self.admin_user)
        self.app_template = self.create_app_template()

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_unauthorized_api_access(self, mock_validate_token):
        mock_validate_token.return_value = None
        url = reverse('app-template-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_creates_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list')
        name = "Test Create Template"
        volume_size_gb = 100
        # Leave out public as it is not required
        data = {
            "image_id": str(uuid.uuid4()),
            "name": name,
            "description": "A test template",
            "short_description": "Test",
            "instantiation_notice": "Notice",
            "script": "Script",
            "ssh_user_requested": True,
            "instantiation_attributes": [
                {"name": "JavaVersion"},
                {"name": "InstallSpringboot"}
            ],
            "account_attributes": [
                {"name": "Username"},
                {"name": "Password"}
            ],
            "security_groups": [
                {"name": "default"},
                {"name": "public"}
            ],
            "volume_size_gb": volume_size_gb,
            "fixed_ram_gb": 1.0,
            "fixed_disk_gb": 10.0,
            "fixed_cores": 1.0,
            "approved": True  # Try to create app_template as public illegally (should end in False)
        }
        response = self.client.post(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], name)
        self.assertFalse(response.data['public'])
        self.assertFalse(response.data['approved'])
        self.assertTrue(response.data['ssh_user_requested'])
        self.assertEqual(response.data['volume_size_gb'], volume_size_gb)
        self.assertEqual(len(response.data['security_groups']), 2)
        self.assertEqual(response.data['security_groups'][0]['name'], "default")
        self.assertEqual(response.data['security_groups'][1]['name'], "public")
        app_template_id = response.data['id']
        # Check that favorite item for self.admin_user and the app_template is created
        self.assertIsNotNone(
            Favorites.objects.filter(app_template_id=app_template_id, user_id=self.admin_user))

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_app_template_creation_via_api_with_missing_fields(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list')
        data = {
            "name": "Incomplete Template",
            "description": "Missing required fields"
        }
        response = self.client.post(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_updates_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-detail', args=[self.app_template.id])
        name = "API Updated Template"
        updated_instantiation_attributes_name = "Updated JavaVersion Field"
        updated_security_group_name = "Updated Default Group"
        data = {
            "name": name,
            "description": "An updated template",
            "short_description": "Updated",
            "instantiation_notice": "Updated Notice",
            "script": "Updated Script",
            "ssh_user_requested": False,
            "instantiation_attributes": [
                {"name": updated_instantiation_attributes_name},
                {"name": "SpringbootVersion"}
            ],
            "account_attributes": [
                {"name": "Username"},
                {"name": "Password"}
            ],
            "security_groups": [
                {"name": updated_security_group_name},
                {"name": "open-access"}
            ],
            "image_id": self.app_template.image_id,
            "approved": True,
            "fixed_ram_gb": 2.0,
            "fixed_disk_gb": 20.0,
            "fixed_cores": 2.0,
        }
        response = self.client.put(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], name)
        self.assertIsNotNone(response.data['updated_at'])
        self.assertFalse(response.data['ssh_user_requested'])
        self.assertEqual(response.data["instantiation_attributes"][0]["name"],
                         updated_instantiation_attributes_name)
        self.assertEqual(len(response.data['security_groups']), 2)
        self.assertEqual(response.data['security_groups'][0]['name'], updated_security_group_name)
        self.assertEqual(response.data['security_groups'][1]['name'], "open-access")
        self.assertEqual(response.data["approved"], False)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_cannot_update_approved_app_template(self, mock_validate_token):
        # Create an approved app template
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        self.app_template.approved = True
        self.app_template.save()

        # Attempt to update the approved template
        url = reverse('app-template-detail', args=[self.app_template.id])
        data = {
            "name": "Updated Name",
            "description": "Updated description",
            "short_description": "Updated",
            "instantiation_notice": "Updated Notice",
            "script": "Updated Script",
            "ssh_user_requested": False,
            "instantiation_attributes": [],
            "account_attributes": [],
            "security_groups": [],
            "image_id": self.app_template.image_id,
            "fixed_ram_gb": 2.0,
            "fixed_disk_gb": 20.0,
            "fixed_cores": 2.0,
        }

        response = self.client.put(url, data, format='json', **self.get_auth_headers())

        # Verify the update was rejected with a 400 Bad Request
        self.assertEqual(response.status_code, 400)
        # Verify that the app template was not updated
        self.assertEqual(AppTemplates.objects.get(id=self.app_template.id).name, self.app_template.name)

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
    def test_list_app_templates_for_admin_with_private_templates(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list') + '?public=False'

        private_app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Private Template",
            description="A private template",
            short_description="Private",
            instantiation_notice="Notice",
            script="Script",
            ssh_user_requested=True,
            creator_id=self.normal_user,
            public=False,
            approved=False,
            volume_size_gb=100,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], private_app_template.name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_list_app_templates_for_private_templates_with_insufficient_rights(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.normal_user.id, 'name': 'User'}
        url = reverse('app-template-list') + '?public=False'

        private_app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Private Template",
            description="A private template",
            short_description="Private",
            instantiation_notice="Notice",
            script="Script",
            creator_id=self.admin_user,
            public=False,
            approved=False,
            volume_size_gb=100,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        response = self.client.get(url, format='json',
                                   **self.get_auth_headers(token="insufficient_rights_token"))
        self.assertEqual(len(response.data), 0)
        self.assertNotIn(private_app_template.id, [template['id'] for template in response.data])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_list_app_templates_for_user_with_search_filter(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list') + '?search=API'

        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.app_template.name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_list_app_templates_for_user_with_public_filter(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list') + '?public=True'

        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.app_template.name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_list_app_templates_for_user_with_approved_filter(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-list') + '?approved=False'

        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.app_template.name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collision(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-check-name-collision', kwargs={'name': self.app_template.name})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['collision'])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collision_no_collision(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-check-name-collision', kwargs={'name': 'No Collision Template'})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['collision'])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_approve_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-approve', args=[self.app_template.id])
        response = self.client.patch(url, format='json', **self.get_auth_headers())
        public_app_template_id = response.data["public_app_template"]["id"]
        self.assertEqual(response.status_code, 200)
        # Old app_template should not be approved and private
        self.assertFalse(AppTemplates.objects.get(id=self.app_template.id).approved)
        self.assertFalse(AppTemplates.objects.get(id=self.app_template.id).public)
        self.assertTrue(AppTemplates.objects.get(id=self.app_template.id).ssh_user_requested)
        self.assertEqual(AppTemplates.objects.all().count(), 2)
        self.assertTrue(AppTemplates.objects.get(id=public_app_template_id).approved)
        self.assertEqual(
            AppTemplateAccountAttributes.objects.filter(app_template_id=public_app_template_id).count(),
            1)
        self.assertEqual(
            AppTemplateInstantiationAttributes.objects.filter(app_template_id=public_app_template_id).count(),
            1)
        self.assertEqual(
            AppTemplateSecurityGroups.objects.filter(app_template_id=public_app_template_id).count(),
            1)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_reject_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.admin_user.id, 'name': 'Admin'}
        url = reverse('app-template-reject', args=[self.app_template.id])
        response = self.client.patch(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AppTemplates.objects.get(id=self.app_template.id).approved)
        self.assertFalse(AppTemplates.objects.get(id=self.app_template.id).public)

    # As soft delete is currently not used, the assert statements are commented out
    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_soft_deletes_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        # instantiation_attribute = AppTemplateInstantiationAttributes.objects.create(
        #    app_template_id=self.app_template,
        #    name="JavaVersion"
        # )

        url = reverse('app-template-detail', args=[self.app_template.id])
        response = self.client.delete(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 204)
        # self.app_template.refresh_from_db()

        # self.assertTrue(self.app_template.deleted)
        # self.assertIsNotNone(self.app_template.deleted_at)
        # instantiation_attribute.refresh_from_db()
        # self.assertIsNotNone(instantiation_attribute.name)


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
        self.assertEqual(1, Favorites.objects.all().count())

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
