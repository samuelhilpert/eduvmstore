import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import Roles


def create_role(role_data: dict) -> Roles:
    """
    Create a new Role entry in the database using Django ORM.

    :param Dict role_data: Dictionary containing the Role details
    :return: The newly created Role object
    :rtype: Roles
    :raises ValidationError: If any required field is missing or invalid
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

    :param str id: The unique identifier of the role to update
    :param dict update_role_data: Dictionary containing the fields to update
    :return: The updated Role object
    :rtype: Roles
    :raises ObjectDoesNotExist: If the Role is not found
    :raises ValidationError: If any field is invalid
    """
    try:
        role = Roles.objects.get(id=id)

        for field, value in update_role_data.items():
            setattr(role, field, value)

        role.save()
        return role
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Role not found")
    except ValidationError as e:
        raise e


def get_role_by_id(id: str) -> Roles:
    """
    Retrieve a Role entry from the database using its ID.

    :param str id: The unique identifier of the role
    :return: The Role object if found
    :rtype: Roles
    :raises ObjectDoesNotExist: If no Role is found with the given ID
    """
    try:
        return Roles.objects.get(id=id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Role with id {id} not found")


def get_role_by_name(name: str) -> Roles:
    """
    Retrieve a Role entry from the database using its ID.

    :param str name: The unique name of the role.
    :return: The Role object if found.
    :raises ObjectDoesNotExist: If no Role is found with the given name.
    """
    try:
        return Roles.objects.get(name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"Role with name {name} not found")
