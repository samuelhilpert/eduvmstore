from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from eduvmstore.db.models import Roles
from eduvmstore.db.operations.roles import create_role, update_role, get_role_by_id
import uuid

class RoleOperationsTests(TestCase):

    def creates_role_successfully(self):
        role_data = {
            "name": "Admin",
            "access_level": 1
        }
        role = create_role(role_data)
        self.assertEqual(role.name, "Admin")
        self.assertEqual(role.access_level, 1)

    def does_not_create_role_with_invalid_data(self):
        role_data = {
            "name": "",
            "access_level": 1
        }
        with self.assertRaises(ValidationError):
            create_role(role_data)

    def updates_role_successfully(self):
        role = Roles.objects.create(
            id=str(uuid.uuid4()),
            name="User",
            access_level=2
        )
        update_data = {
            "name": "SuperUser",
            "access_level": 3
        }
        updated_role = update_role(role.id, update_data)
        self.assertEqual(updated_role.name, "SuperUser")
        self.assertEqual(updated_role.access_level, 3)

    def does_not_update_nonexistent_role(self):
        update_data = {
            "name": "NonExistent",
            "access_level": 4
        }
        with self.assertRaises(ObjectDoesNotExist):
            update_role(str(uuid.uuid4()), update_data)

    def retrieves_role_by_id_successfully(self):
        role = Roles.objects.create(
            id=str(uuid.uuid4()),
            name="Viewer",
            access_level=1
        )
        retrieved_role = get_role_by_id(role.id)
        self.assertEqual(retrieved_role.name, "Viewer")
        self.assertEqual(retrieved_role.access_level, 1)

    def does_not_retrieve_nonexistent_role(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_role_by_id(str(uuid.uuid4()))