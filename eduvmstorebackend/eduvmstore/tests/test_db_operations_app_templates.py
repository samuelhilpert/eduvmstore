import uuid
from django.test import TestCase
from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes, \
    AppTemplateAccountAttributes
from eduvmstore.db.operations.app_templates import (
    check_name_collision, approve_app_template, soft_delete_app_template, reject_app_template,
    CollisionReason)


class AppTemplateOperationsTests(TestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user

    def create_app_template(self, user, name="Test Template"):
        app_template = AppTemplates.objects.create(
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
        )
        AppTemplateInstantiationAttributes.objects.create(
            app_template_id=app_template,
            name="JavaVersion"
        )
        AppTemplateAccountAttributes.objects.create(
            app_template_id=app_template,
            name="Username"
        )
        return app_template

    def setUp(self):
        self.user = self.create_user_and_role()
        self.app_template = self.create_app_template(self.user)

    def test_checks_direct_name_collision(self):
        collision, reason, context = check_name_collision(self.app_template.name)
        self.assertTrue(collision)
        self.assertEqual(reason, CollisionReason.DIRECT_MATCH)

    def test_checks_name_collision_with_versioned_templates(self):
        base_name = "Template"
        self.create_app_template(self.user, name=base_name + "-V1")
        collision, reason, context = check_name_collision(base_name)
        # Base name should also be a collision
        self.assertTrue(collision)
        self.assertEqual(reason, CollisionReason.VERSIONED_TEMPLATE_EXISTS)

    def test_name_collision_with_version_suffix(self):
        suffix = "-V23"
        app_template_name = "innocent_name" + suffix
        collision, reason, context = check_name_collision(app_template_name)
        self.assertTrue(collision)
        self.assertEqual(reason, CollisionReason.VERSION_SUFFIX_RESERVED)

    def test_no_name_collision(self):
        collision, reason, context = check_name_collision("NoCollision")
        self.assertFalse(collision)
        self.assertEqual(reason, CollisionReason.NO_COLLISION)

    def test_approves_app_template_successfully(self):
        approved_app_template = approve_app_template(self.app_template.id)

        self.assertEqual(AppTemplates.objects.count(), 2)
        self.assertTrue(approved_app_template.approved)
        self.app_template.refresh_from_db()
        self.assertFalse(self.app_template.public)
        self.assertEqual(approved_app_template.version, 1)
        self.assertEqual(self.app_template.version, 2)
        expected_name = self.app_template.name + "-V1"
        self.assertEqual(approved_app_template.name, expected_name)
        self.assertTrue(AppTemplates.objects.get(id=approved_app_template.id).approved)
        self.assertEqual(
            AppTemplateAccountAttributes.objects.filter(app_template_id=approved_app_template.id).count(),
            1)
        self.assertEqual(
            AppTemplateInstantiationAttributes.objects.filter(
                app_template_id=approved_app_template.id).count(),
            1)

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
