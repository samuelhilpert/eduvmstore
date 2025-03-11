import uuid
from django.utils.timezone import now
from django.test import TestCase

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles

class AppTemplatesModelTests(TestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def test_creates_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Test Template",
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
        self.assertEqual(app_template.name, "Test Template")
        self.assertFalse(app_template.deleted)
        self.assertEqual(app_template.version, "1.0")

    def test_does_not_create_app_template_with_duplicate_name(self):
        user = self.create_user_and_role()
        AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Duplicate Template",
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
        with self.assertRaises(Exception):
            AppTemplates.objects.create(
                image_id=uuid.uuid4(),
                name="Duplicate Template",
                description="Another test template",
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

    def test_updates_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Update Template",
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
        app_template.name = "Updated Template"
        app_template.save()
        self.assertEqual(app_template.name, "Updated Template")

    def test_soft_deletes_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            image_id=uuid.uuid4(),
            name="Delete Template",
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
        app_template.deleted = True
        app_template.deleted_at = now()
        app_template.save()
        self.assertTrue(app_template.deleted)
        self.assertIsNotNone(app_template.deleted_at)