from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Users, Roles
from eduvmstore.db.operations.users import create_user, get_user_by_id, list_users, update_user_role, soft_delete_user
import uuid

class UserOperationsTests(TestCase):

    def create_role(self):
        return Roles.objects.create(name="Admin", access_level=1)

    def creates_user_successfully(self):
        role = self.create_role()
        user = create_user(str(uuid.uuid4()), role.id)
        self.assertEqual(user.role_id, role.id)
        self.assertFalse(user.deleted)

    def does_not_create_user_with_invalid_data(self):
        with self.assertRaises(ValidationError):
            create_user("", None)

    def retrieves_user_by_id_successfully(self):
        role = self.create_role()
        user = create_user(str(uuid.uuid4()), role.id)
        retrieved_user = get_user_by_id(user.id)
        self.assertEqual(retrieved_user.id, user.id)

    def does_not_retrieve_nonexistent_user(self):
        self.assertIsNone(get_user_by_id(str(uuid.uuid4())))

    def lists_all_users(self):
        role = self.create_role()
        create_user(str(uuid.uuid4()), role.id)
        users = list_users()
        self.assertEqual(len(users), 1)

    def updates_user_role_successfully(self):
        role1 = self.create_role()
        role2 = Roles.objects.create(name="User", access_level=2)
        user = create_user(str(uuid.uuid4()), role1.id)
        updated_user = update_user_role(user.id, role2.id)
        self.assertEqual(updated_user.role_id, role2.id)

    def does_not_update_role_of_nonexistent_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            update_user_role(str(uuid.uuid4()), str(uuid.uuid4()))

    def soft_deletes_user_successfully(self):
        role = self.create_role()
        user = create_user(str(uuid.uuid4()), role.id)
        soft_delete_user(user.id)
        user.refresh_from_db()
        self.assertTrue(user.deleted)
        self.assertIsNotNone(user.deleted_at)