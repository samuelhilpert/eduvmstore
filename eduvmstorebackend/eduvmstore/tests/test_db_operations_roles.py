import uuid
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Roles
from eduvmstore.db.operations.roles import create_role, update_role, get_role_by_id, get_role_by_name

class RoleOperationsTests(TestCase):

    def setUp(self):
        self.role_name = "Admin"
        self.access_level = 6000
        self.role = Roles.objects.create(
            id=str(uuid.uuid4()),
            name=self.role_name,
            access_level=self.access_level
        )

    def test_creates_role_successfully(self):
        role_data = {
            "name": "NewRole",
            "access_level": 5000
        }
        role = create_role(role_data)
        self.assertEqual(role.name, "NewRole")
        self.assertEqual(role.access_level, 5000)

    def test_does_not_create_role_with_invalid_data(self):
        role_data = {
            "name": "",
            "access_level": 6000
        }
        with self.assertRaises(ValidationError):
            create_role(role_data)

    def test_updates_role_successfully(self):
        update_name = "SuperUser"
        update_access_level = 3000
        update_data = {
            "name": update_name,
            "access_level": update_access_level
        }
        updated_role = update_role(self.role.id, update_data)
        self.assertEqual(updated_role.name, update_name)
        self.assertEqual(updated_role.access_level, update_access_level)

    def test_does_not_update_nonexistent_role(self):
        update_data = {
            "name": "NonExistent",
            "access_level": 4
        }
        with self.assertRaises(ObjectDoesNotExist):
            update_role(str(uuid.uuid4()), update_data)

    def test_retrieves_role_by_id_successfully(self):
        retrieved_role = get_role_by_id(self.role.id)
        self.assertEqual(retrieved_role.name, self.role_name)
        self.assertEqual(retrieved_role.access_level, self.access_level)

    def test_does_not_retrieve_nonexistent_role(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_role_by_id(str(uuid.uuid4()))

    def test_retrieves_role_by_name_successfully(self):
        retrieved_role = get_role_by_name(self.role_name)
        self.assertEqual(retrieved_role.name, self.role_name)
        self.assertEqual(retrieved_role.access_level, self.access_level)

    def test_does_not_retrieve_nonexistent_role_by_name(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_role_by_name("NonExistentRole")