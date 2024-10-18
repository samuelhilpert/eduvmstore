import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import Roles

def create_role(role_data: dict) -> Roles:
    """
    Create a new Role entry in the database using Django ORM.
    """
    if not role_data['name']:
        raise ValidationError("Role name cannot be empty")
    if role_data['access_level'] is None:
        raise ValidationError("Access level cannot be empty")

    try:
        new_role = Roles.objects.create(
            id=str(uuid.uuid4()),  # Generate unique UUID
            name=role_data['name'],
            access_level=role_data['access_level']
        )
        return new_role
    except ValidationError as e:
        raise e


def update_role(id: str, update_role_data: dict) -> Roles:
    """
    Update an existing Role entry in the database using Django ORM.

    :param id: The unique identifier of the role to update
    :param update_role_data: Dictionary containing the fields to update
           (e.g., {"name": "new_name", "access_level": 2000})
    :return: The updated Role object
    """
    try:
        role = Roles.objects.get(id=id)  # Fetch role by ID

        # Update the fields provided in the dictionary
        for field, value in update_role_data.items():
            setattr(role, field, value)  # Dynamically set attributes

        role.save()  # Save changes
        return role
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Role not found")
    except ValidationError as e:
        raise e

def get_role_by_id(id: str) -> Roles:
    """
    Retrieve a Role entry from the database using its ID.

    :param id: The unique identifier of the role.
    :return: The Role object if found.
    :raises ObjectDoesNotExist: If no Role is found with the given ID.
    """
    try:
        return Roles.objects.get(id=id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Role with id {id} not found")
