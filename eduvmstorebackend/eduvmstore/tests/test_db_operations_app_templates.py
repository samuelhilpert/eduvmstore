from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import AppTemplates, Users, Roles, AppTemplateInstantiationAttributes
from eduvmstore.db.operations.app_templates import (
    check_app_template_name_collisions, approve_app_template, soft_delete_app_template, reject_app_template
)
import uuid

class AppTemplateOperationsTests(TestCase):

    def create_user_and_role(self):
        role = Roles.objects.create(name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
                                    access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"))
        user = Users.objects.create(role_id=role)
        return user


    def test_checks_name_collisions(self):
        user = self.create_user_and_role()
        AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Collision Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            image_id=str(uuid.uuid4()),
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5
        )
        collision = check_app_template_name_collisions("Collision Template")
        self.assertTrue(collision)

    def test_approves_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Approve Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            image_id=str(uuid.uuid4()),
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5,
            approved=False
        )
        approved_template = approve_app_template(app_template.id)
        self.assertTrue(approved_template.approved)

    def test_rejects_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Approve Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            image_id=str(uuid.uuid4()),
            creator_id=user,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
            per_user_ram_gb=0.5,
            per_user_disk_gb=5.0,
            per_user_cores=0.5,
            approved=False
        )
        rejected_app_template = reject_app_template(app_template.id)
        self.assertFalse(rejected_app_template.approved)
        self.assertFalse(rejected_app_template.public)

    def test_soft_deletes_app_template_successfully(self):
        user = self.create_user_and_role()
        app_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Delete Template",
            description="A test template",
            short_description="Test",
            instantiation_notice="Notice",
            script="Script",
            image_id=str(uuid.uuid4()),
            creator_id=user,
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
        soft_delete_app_template(app_template.id)
        app_template.refresh_from_db()
        self.assertTrue(app_template.deleted)
        self.assertIsNotNone(app_template.deleted_at)
        instantiation_attribute.refresh_from_db()
        self.assertIsNotNone(instantiation_attribute)