from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Roles
from eduvmstore.db.operations.roles import create_role, update_role, get_role_by_id
import uuid

class RoleOperationsTests(TestCase):

    def test_creates_role_successfully(self):
        name = "Admin"
        access_level = 6000
        role_data = {
            "name": name,
            "access_level": access_level
        }
        role = create_role(role_data)
        self.assertEqual(role.name, name)
        self.assertEqual(role.access_level, access_level)

    def test_does_not_create_role_with_invalid_data(self):
        role_data = {
            "name": "",
            "access_level": 6000
        }
        with self.assertRaises(ValidationError):
            create_role(role_data)

    def test_updates_role_successfully(self):
        role = Roles.objects.create(
            id=str(uuid.uuid4()),
            name="User",
            access_level=1000
        )
        update_name = "SuperUser"
        update_access_level = 3000
        update_data = {
            "name": update_name,
            "access_level": update_access_level
        }
        updated_role = update_role(role.id, update_data)
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
        role = Roles.objects.create(
            id=str(uuid.uuid4()),
            name="Viewer",
            access_level=1
        )
        retrieved_role = get_role_by_id(role.id)
        self.assertEqual(retrieved_role.name, "Viewer")
        self.assertEqual(retrieved_role.access_level, 1)

    def test_does_not_retrieve_nonexistent_role(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_role_by_id(str(uuid.uuid4()))