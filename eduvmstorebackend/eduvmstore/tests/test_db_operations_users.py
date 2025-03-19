from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Roles
from eduvmstore.db.operations.users import create_user, get_user_by_id, soft_delete_user
import uuid

class UserOperationsTests(TestCase):

    def create_role(self):
        return Roles.objects.create(name="EduVMStoreAdmin", access_level=7000)

    def setUp(self):
        self.role = self.create_role()

    def test_creates_user_successfully(self):
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": self.role
        }
        user = create_user(user_data)
        self.assertEqual(user.role_id, self.role)
        self.assertFalse(user.deleted)

    def test_does_not_create_user_with_invalid_data(self):
        user_data = {
            "id": "",
            "role_id": None
        }
        with self.assertRaises(ValidationError):
            create_user(user_data)

    def test_retrieves_user_by_id_successfully(self):
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": self.role
        }
        user = create_user(user_data)
        retrieved_user = get_user_by_id(user.id)
        self.assertEqual(str(retrieved_user.id), user.id)

    def test_does_not_retrieve_nonexistent_user(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_user_by_id(str(uuid.uuid4()))

    def test_soft_deletes_user_successfully(self):
        user_data = {
            "id": str(uuid.uuid4()),
            "role_id": self.role
        }
        user = create_user(user_data)
        soft_delete_user(user.id)
        user.refresh_from_db()
        self.assertTrue(user.deleted)
        self.assertIsNotNone(user.deleted_at)