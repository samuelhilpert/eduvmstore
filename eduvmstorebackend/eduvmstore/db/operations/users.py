from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import Users

def create_user(user_data: dict) -> Users:
    """
    Create a new User entry in the database using Django ORM.

    :param dict user_data: Dictionary containing the User details
    :return: The newly created User object
    :rtype: Users
    :raises ValidationError: If any required field is missing or invalid
    """
    if not user_data.get('id'):
        raise ValidationError("User ID cannot be empty")
    if not user_data.get('role_id'):
        raise ValidationError("Role ID cannot be empty")

    try:
        new_user = Users.objects.create(
            id=user_data['id'],
            role_id=user_data['role_id'],
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted=False
        )
        return new_user
    except ValidationError as e:
        raise e

def get_user_by_id(id: str) -> Users:
    """
    Retrieve a User entry from the database using its ID.

    :param str id: The unique identifier of the user
    :return: The User object if found
    :rtype: Users
    :raises ObjectDoesNotExist: If no User is found with the given ID
    """
    try:
        return Users.objects.get(id=id, deleted=False)
    except ObjectDoesNotExist:
        return None


def list_users() -> list[Users]:
    """
    Retrieve all User records from the database.

    :return: A list of User objects
    :rtype: list[Users]
    """
    return Users.objects.filter(deleted=False)

def update_user_role(id: str, role_id: str) -> Users:
    """
    Update the role of a specific User by ID.

    :param str id: The UUID of the User
    :param str role_id: The UUID of the new Role
    :return: The updated User object
    :rtype: Users
    :raises ObjectDoesNotExist: If the User or Role is not found
    """
    try:
        user = Users.objects.get(id=id, deleted=False)
        user.role_id = role_id
        user.updated_at = timezone.now()
        user.save()
        return user
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User or Role not found.")


def soft_delete_user(id: str) -> None:
    """
    Soft delete a User by marking them as deleted.

    :param str id: The UUID of the User
    :return: None
    :rtype: None
    :raises ObjectDoesNotExist: If the User is not found
    """
    try:
        user = Users.objects.get(id=id, deleted=False)
        user.deleted = True
        user.deleted_at = timezone.now()
        user.updated_at = user.deleted_at
        user.save()
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User not found.")
