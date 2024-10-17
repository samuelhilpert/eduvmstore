from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import Users
def create_user(id: str, role_id: int) -> Users:
    """
    Create a new User entry in the database.

    :param id: The ID of the new User from keystone
    :param role_id: The ID of the Role associated with the new User
    """
    try:
        new_user = Users.objects.create(
            id=id,
            role_id=role_id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted=False
        )
        return new_user
    except ValidationError as e:
        raise e

def get_user_by_id(id: str) -> Users:
    """
    Retrieve a User entry from the database by ID.

    :param id: The ID of the User to retrieve
    :return: The User object if found, None otherwise
    """
    try:
        return Users.objects.get(id=id, deleted=False)
    except ObjectDoesNotExist:
        return None


def list_users() -> list[Users]:
    """
    Retrieve all User records from the database.

    :return: A list of User objects
    """
    return Users.objects.filter(deleted=False)

def update_user_role(id: str, role_id: str) -> Users:
    """
    Update the role of a specific User by ID.

    :param id: The UUID of the User
    :param role_id: The UUID of the new Role
    :return: The updated User object
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

    :param user_id: The UUID of the User
    """
    try:
        user = Users.objects.get(id=id, deleted=False)
        user.deleted = True
        user.deleted_at = timezone.now()
        user.updated_at = user.deleted_at
        user.save()
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User not found.")
