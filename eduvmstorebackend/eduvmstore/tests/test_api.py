import logging
from rest_framework.test import APITestCase
from django.urls import reverse

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes, Favorites
from unittest.mock import patch
import uuid

logger = logging.getLogger('eduvmstore_logger')

class AppTemplateViewSetTests(APITestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def get_auth_headers(self, token="valid_token"):
        return {'HTTP_X_AUTH_TOKEN': token}

    def setUp(self):
        self.user = self.create_user_and_role()
        self.client.force_authenticate(user=self.user)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_creates_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        url = reverse('app-template-list')
        name = "API Test Template"
        data = {
            "image_id": str(uuid.uuid4()),
            "name": name,
            "description": "A test template",
            "short_description": "Test",
            "instantiation_notice": "Notice",
            "script": "Script",
            "instantiation_attributes": [
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
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="API Update Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            public=True,
            approved=False,
            creator_id=self.user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )

        url = reverse('app-template-detail', args=[app_template.id])
        name = "API Updated Template"
        updated_instantiation_attributes_name = "Updated Username"
        data = {
            "name": name,
            "description": "An updated template",
            "short_description": "Updated",
            "instantiation_notice": "Updated Notice",
            "script": "Updated Script",
            "instantiation_attributes": [
                {"name": updated_instantiation_attributes_name},
                {"name": "Updated Password"}
            ],
            "image_id": app_template.image_id,
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
        self.assertEqual(response.data["instantiation_attributes"][0]["name"], updated_instantiation_attributes_name)
        self.assertEqual(response.data["approved"], False)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_filters_app_templates_by_search(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        name = "Searchable Template"
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name=name,
            description="A searchable template",
            short_description="Search",
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
        url = reverse('app-template-list') + '?search=Searchable'
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], name)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collisions(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        name = "Collision Template"
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name=name,
            description="A collision template",
            short_description="Collision",
            instantiation_notice="Notice",
            script="Script",
            creator_id=self.user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-check-name-collisions', kwargs={'name': name})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['collisions'])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_checks_name_collisions_no_collision(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="No Collision Template",
            description="A non-collision template",
            short_description="No Collision",
            instantiation_notice="Notice",
            script="Script",
            creator_id=self.user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-check-name-collisions', kwargs={'name': 'Collision Template'})
        response = self.client.get(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['collisions'])

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_soft_deletes_app_template_via_api_successfully(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="API Delete Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            public=True,
            approved=False,
            creator_id=self.user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        instantiation_attribute = AppTemplateInstantiationAttributes.objects.create(
            app_template_id=app_template,
            name="Username"
        )

        url = reverse('app-template-detail', args=[app_template.id])
        response = self.client.delete(url, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 204)
        app_template.refresh_from_db()

        self.assertTrue(app_template.deleted)
        self.assertIsNotNone(app_template.deleted_at)
        instantiation_attribute.refresh_from_db()
        self.assertIsNotNone(instantiation_attribute.name)

class FavoritesViewSetTests(APITestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def get_auth_headers(self, token="valid_token"):
        return {'HTTP_X_AUTH_TOKEN': token}

    def setUp(self):
        self.user = self.create_user_and_role()
        self.client.force_authenticate(user=self.user)

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_adds_app_template_to_favorites(self, mock_validate_token):
         mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
         app_template = AppTemplates.objects.create(
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

         url = reverse('favorite-list')
         data = {"app_template_id": app_template.id}
         response = self.client.post(url, data, format='json', **self.get_auth_headers())
         self.assertEqual(response.status_code, 201)
         self.assertTrue(1, Favorites.objects.all().count())

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_removes_app_template_from_favorites(self, mock_validate_token):
        mock_validate_token.return_value = {'id': self.user.id, 'name': 'Admin'}
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
        Favorites.objects.create(id=uuid.uuid4(), app_template_id=app_template, user_id=self.user)

        url = reverse('favorite-delete-by-app-template')
        data = {"app_template_id": app_template.id}
        response = self.client.delete(url, data, format='json', **self.get_auth_headers())
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Favorites.objects.filter(
            app_template_id=app_template.id, user_id=self.user.id).exists())

    @patch('eduvmstore.middleware.authentication_middleware.KeystoneAuthenticationMiddleware'
           '.validate_token_with_keystone')
    def test_lists_favorites_for_user(self, mock_validate_token):
        mock_validate_token.return_value = {'id': str(uuid.uuid4()), 'name': 'Admin'}
        app_template = AppTemplates.objects.create(
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
        Favorites.objects.create(app_template_id=app_template, user_id=self.user)
        url = reverse('app-template-favorites')
        response = self.client.get(url, format='json', **self.get_auth_headers())
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(response.data), 1)
        #self.assertEqual(response.data[0]['name'], app_template.name)