from rest_framework.test import APITestCase
from django.urls import reverse
from eduvmstore.db.models import AppTemplates, Users, Roles
import uuid

class AppTemplateViewSetTests(APITestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name="Admin", access_level=6000)
        user = Users.objects.create(role_id=role)
        return user

    def test_creates_app_template_via_api_successfully(self):
        user = self.create_user_and_role()
        self.client.force_authenticate(user=user)
        url = reverse('app-template-list')
        name = "API Test Template"
        data = {
            "image_id": str(uuid.uuid4()),
            "creator_id": user.id,
            "name": name,
            "description": "A test template",
            "short_description": "Test",
            "instantiation_notice": "Notice",
            "fixed_ram_gb": 1.0,
            "fixed_disk_gb": 10.0,
            "fixed_cores": 1.0,
            "per_user_ram_gb": 0.5,
            "per_user_disk_gb": 5.0,
            "per_user_cores": 0.5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], name)

    def test_filters_app_templates_by_search(self):
        user = self.create_user_and_role()
        self.client.force_authenticate(user=user)
        name = "Searchable Template"
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name=name,
            description="A searchable template",
            short_description="Search",
            instantiation_notice="Notice",
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-list') + '?search=Searchable'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], name)

    def test_checks_name_collisions(self):
        user = self.create_user_and_role()
        self.client.force_authenticate(user=user)
        name = "Collision Template"
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name=name,
            description="A collision template",
            short_description="Collision",
            instantiation_notice="Notice",
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-check-name-collisions', kwargs={'name': name})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['collisions'])

    def test_checks_name_collisions_no_collision(self):
        user = self.create_user_and_role()
        self.client.force_authenticate(user=user)
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="No Collision Template",
            description="A non-collision template",
            short_description="No Collision",
            instantiation_notice="Notice",
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-check-name-collisions', kwargs={'name': 'Collision Template'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['collisions'])

    def test_soft_deletes_app_template_via_api_successfully(self):
        user = self.create_user_and_role()
        self.client.force_authenticate(user=user)
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="API Delete Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        url = reverse('app-template-detail', args=[app_template.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        app_template.refresh_from_db()
        self.assertTrue(app_template.deleted)
        self.assertIsNotNone(app_template.deleted_at)