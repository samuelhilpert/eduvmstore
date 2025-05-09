from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import Roles, Users, AppTemplates
from eduvmstore.db.operations.users import (create_user, get_user_by_id, soft_delete_user, delete_user)
import uuid


class UserOperationsTests(TestCase):

    def create_user_and_role(self):
        admin_role = Roles.objects.create(
            name=DEFAULT_ROLES.get("EduVMStoreAdmin").get("name"),
            access_level=DEFAULT_ROLES.get("EduVMStoreAdmin").get("access_level"),
        )
        user_role = Roles.objects.create(
            name=DEFAULT_ROLES.get("EduVMStoreUser").get("name"),
            access_level=DEFAULT_ROLES.get("EduVMStoreUser").get("access_level"),
        )
        admin_user = Users.objects.create(role_id=admin_role)
        normal_user = Users.objects.create(role_id=user_role)
        self.admin_role= admin_role
        self.user_role = user_role
        self.admin_user = admin_user
        self.normal_user = normal_user

    def setUp(self):
        self.create_user_and_role()

    def test_creates_user_successfully(self):
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": self.admin_role
        }
        user = create_user(user_data)
        self.assertEqual(user.role_id, self.admin_role)
        self.assertFalse(user.deleted)

    def test_does_not_create_user_with_invalid_data(self):
        user_data = {
            "id": "",
            "role_id": None
        }
        with self.assertRaises(ValidationError):
            create_user(user_data)

    def test_retrieves_user_by_id_successfully(self):
        retrieved_user = get_user_by_id(self.admin_user.id)
        self.assertEqual(retrieved_user.id, self.admin_user.id)

    def test_does_not_retrieve_nonexistent_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_user_by_id(str(uuid.uuid4()))

    def test_soft_deletes_user_successfully(self):
        soft_delete_user(self.admin_user.id)
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.deleted)
        self.assertIsNotNone(self.admin_user.deleted_at)

    def test_delete_user_with_private_templates(self):
        # Create private template owned by target user
        private_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Private Template",
            image_id=str(uuid.uuid4()),
            description="A private template",
            short_description="Private",
            creator_id=self.normal_user,
            public=False,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        # Delete the user
        delete_user(self.normal_user, self.admin_user)

        # Check that user is deleted
        self.assertFalse(Users.objects.filter(id=self.normal_user.id).exists())

        # Check that private templates are deleted
        self.assertFalse(AppTemplates.objects.filter(id=private_template.id).exists())

    def test_delete_user_with_public_templates_transfers_ownership(self):
        # Create public template owned by target user
        public_app_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            image_id=str(uuid.uuid4()),
            name="Public Template",
            description="A public template",
            short_description="Public",
            creator_id=self.normal_user,
            public=True,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        # Track the original updated_at time
        original_updated_at = public_app_template.updated_at

        # Delete the user
        delete_user(self.normal_user, self.admin_user)

        # Check that user is deleted
        self.assertFalse(Users.objects.filter(id=self.normal_user.id).exists())

        # Check that public template ownership was transferred
        public_app_template.refresh_from_db()
        self.assertEqual(public_app_template.creator_id.id, self.admin_user.id)
        self.assertNotEqual(public_app_template.updated_at, original_updated_at)

    def test_user_cannot_delete_self_with_public_templates(self):
        # Create public template owned by the user
        AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Public Template",
            image_id=str(uuid.uuid4()),
            description="A public template",
            short_description="Public",
            creator_id=self.admin_user,
            public=True,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        # Try to delete self
        with self.assertRaises(ValidationError) as context:
            delete_user(self.admin_user, self.admin_user)

        # Check error message
        self.assertIn("Cannot delete your own user while public AppTemplates are assigned to you",
                      str(context.exception))

        # Verify user still exists
        self.assertTrue(Users.objects.filter(id=self.admin_user.id).exists())

    def test_user_can_delete_self_with_only_private_templates(self):
        # Create private template owned by the user
        private_template = AppTemplates.objects.create(
            id=str(uuid.uuid4()),
            name="Private Template",
            image_id=str(uuid.uuid4()),
            description="A private template",
            short_description="Private",
            creator_id=self.admin_user,
            public=False,
            fixed_ram_gb=1.0,
            fixed_disk_gb=10.0,
            fixed_cores=1.0,
        )

        # Delete self
        delete_user(self.admin_user, self.admin_user)

        # Check that user is deleted
        self.assertFalse(Users.objects.filter(id=self.admin_user.id).exists())

        # Check that private templates are deleted
        self.assertFalse(AppTemplates.objects.filter(id=private_template.id).exists())