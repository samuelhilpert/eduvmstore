import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import Role

def create_role(data: dict) -> Role:
    """
    Create a new Role entry in the database using Django ORM.
    """
    try:
        new_role = Role.objects.create(
            id=str(uuid.uuid4()),  # Generate unique UUID
            name=data['name'],
            access_level=data['access_level']
        )
        return new_role
    except ValidationError as e:
        raise e

def update_role(id: str, name: str = None, access_level: int = None) -> Role:
    """
    Update an existing Role entry in the database using Django ORM.
    """
    try:
        role = Role.objects.get(id=id)  # Fetch role by ID
        if name:
            role.name = name
        if access_level:
            role.access_level = access_level

        role.save()  # Save changes
        return role
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Role not found")
    except ValidationError as e:
        raise e

def get_role_by_id(id: str) -> Role:
    """
    Retrieve a Role entry from the database using its ID.

    :param id: The unique identifier of the role.
    :return: The Role object if found.
    :raises ObjectDoesNotExist: If no Role is found with the given ID.
    """
    try:
        return Role.objects.get(id=id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Role with id {id} not found")
