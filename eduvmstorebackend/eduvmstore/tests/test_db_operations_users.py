from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Users, Roles
from eduvmstore.db.operations.users import create_user, get_user_by_id, list_users, update_user_role, soft_delete_user
import uuid

class UserOperationsTests(TestCase):

    def create_role(self):
        return Roles.objects.create(name="Admin", access_level=6000)

    def test_creates_user_successfully(self):
        role = self.create_role()
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": role
        }
        user = create_user(user_data)
        self.assertEqual(user.role_id, role)
        self.assertFalse(user.deleted)

    def test_does_not_create_user_with_invalid_data(self):
        user_data = {
            "id": "",
            "role_id": None
        }
        with self.assertRaises(ValidationError):
            create_user(user_data)

    def test_retrieves_user_by_id_successfully(self):
        role = self.create_role()
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": role
        }
        user = create_user(user_data)
        retrieved_user = get_user_by_id(user.id)
        self.assertEqual(str(retrieved_user.id), user.id)

    def test_does_not_retrieve_nonexistent_user(self):
        self.assertIsNone(get_user_by_id(str(uuid.uuid4())))

    def test_lists_all_users(self):
        role = self.create_role()
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": role
        }
        create_user(user_data)
        users = list_users()
        self.assertEqual(len(users), 1)

    def test_updates_user_role_successfully(self):
        role1 = self.create_role()
        role2 = Roles.objects.create(name="User", access_level=1000)
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": role1
        }
        user = create_user(user_data)
        updated_user = update_user_role(user.id, role2)
        self.assertEqual(updated_user.role_id, role2)

    def test_does_not_update_role_of_nonexistent_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            update_user_role(str(uuid.uuid4()), str(uuid.uuid4()))

    def test_soft_deletes_user_successfully(self):
        role = self.create_role()
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": role
        }
        user = create_user(user_data)
        soft_delete_user(user.id)
        user.refresh_from_db()
        self.assertTrue(user.deleted)
        self.assertIsNotNone(user.deleted_at)