import uuid
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes
from eduvmstore.db.operations.app_templates import (
    check_app_template_name_collisions, approve_app_template, soft_delete_app_template, reject_app_template,
    has_version_suffix
)

class AppTemplateOperationsTests(TestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def create_app_template(self, user, name="Test Template"):
        return AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name=name,
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            image_id=str(uuid.uuid4()),
            creator_id=user,
            public=True,
            approved=False,
            volume_size_gb=100,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5,
        )

    def setUp(self):
        self.user = self.create_user_and_role()
        self.app_template = self.create_app_template(self.user)

    def test_checks_name_collisions(self):
        collision = check_app_template_name_collisions(self.app_template.name)
        self.assertTrue(collision)
        collisionVersionSuffix = check_app_template_name_collisions(self.app_template.name + "-V3")
        self.assertTrue(collisionVersionSuffix)

    def test_has_version_suffix(self):
        # Should return True for names with proper version suffixes
        self.assertTrue(has_version_suffix("example-V21"))
        self.assertTrue(has_version_suffix("template-V1"))
        self.assertTrue(has_version_suffix("long name with spaces-V0"))
        self.assertTrue(has_version_suffix("name-V999"))

        # Should return False for names without version suffixes
        self.assertFalse(has_version_suffix("app_templateITIL3"))
        self.assertFalse(has_version_suffix("V1"))  # No hyphen
        self.assertFalse(has_version_suffix("template-v1"))  # Lowercase v
        self.assertFalse(has_version_suffix("template-V"))  # No digits
        self.assertFalse(has_version_suffix("template-V1a"))  # Non-digit after number
        self.assertFalse(has_version_suffix("template-V1-suffix"))  # Something after
        self.assertFalse(has_version_suffix("template V1"))  # Space instead of hyphen

    def test_approves_app_template_successfully(self):
        approved_template = approve_app_template(self.app_template.id)

        self.assertEqual(AppTemplates.objects.count(),2)
        self.assertTrue(approved_template.approved)
        self.app_template.refresh_from_db()
        self.assertFalse(self.app_template.public)
        self.assertEqual(approved_template.version, 1)
        self.assertEqual(self.app_template.version, 2)
        expected_name = self.app_template.name + "-V1"
        self.assertEqual(approved_template.name, expected_name)

    def test_rejects_app_template_successfully(self):
        rejected_app_template = reject_app_template(self.app_template.id)
        self.assertFalse(rejected_app_template.approved)
        self.assertFalse(rejected_app_template.public)

    def test_soft_deletes_app_template_successfully(self):
        instantiation_attribute = AppTemplateInstantiationAttributes.objects.create(
            app_template_id=self.app_template,
            name="Username"
        )
        soft_delete_app_template(self.app_template.id)
        self.app_template.refresh_from_db()
        self.assertTrue(self.app_template.deleted)
        self.assertIsNotNone(self.app_template.deleted_at)
        instantiation_attribute.refresh_from_db()
        self.assertIsNotNone(instantiation_attribute)