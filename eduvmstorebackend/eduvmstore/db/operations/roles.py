import uuid
from django.db import transaction
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
        raise Exception("Role not found")
    except ValidationError as e:
        raise e
