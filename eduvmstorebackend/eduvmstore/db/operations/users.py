from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from eduvmstore.config.access_levels import DEFAULT_ROLES
from eduvmstore.db.models import Users, AppTemplates
from eduvmstore.db.operations.roles import get_role_by_name, create_role

from typing import Dict


def create_user(user_data: Dict) -> Users:
    """
    Create a new User entry in the database using Django ORM. The role can either be specified by ID or name
        according to the default roles in eduvmstore/config/access_levels.py.
        If the default role is not found,
        this role is created.

    :param Dict user_data: Dictionary containing the User details. This is either id and role_id or id
        and role_name.
        The role name is matched to the default roles in eduvmstore/config/access_levels.py
    :return: The newly created User object
    :rtype: Users
    :raises ValidationError: If any required field is missing or invalid
    """
    if not user_data.get('id'):
        raise ValidationError("User ID cannot be empty")

    # Only if no role ID is given match the role name to the default roles
    if not user_data.get('role_id'):
        # match statement -> extensibility with further roles, add them in eduvmstore/config/access_levels.py
        match user_data.get('keystone_role_name').lower():
            case 'admin':
                role_name = DEFAULT_ROLES['EduVMStoreAdmin']['name']
                default_access_level = DEFAULT_ROLES['EduVMStoreAdmin']['access_level']
            case _:
                role_name = DEFAULT_ROLES['EduVMStoreUser']['name']
                default_access_level = DEFAULT_ROLES['EduVMStoreUser']['access_level']

        try:
            role_id = get_role_by_name(role_name)
        except ObjectDoesNotExist:
            role_id = create_role({'name': role_name, 'access_level': default_access_level})

        user_data['role_id'] = role_id

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
    Retrieve a User entry from the database using its ID, including role information.

    :param str id: The unique identifier of the user
    :return: The User object if found, with role information accessible
    :rtype: Users
    :raises ObjectDoesNotExist: If no User is found with the given ID
    """
    try:
        return Users.objects.select_related('role_id').get(id=id, deleted=False)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with id {id} not found.")

@transaction.atomic
def delete_user(user_to_delete: Users, current_user: Users = None) -> None:
    """
    Delete a user and handle their AppTemplates:
    - Private AppTemplates: deleted (related objects are deleted automatically via model cascade)
    - Public AppTemplates: transferred to the deleting admin user as updated creator
    - If the user is deleting themselves and has public AppTemplates, raise a ValidationError

    :param str user_to_delete_id: The UUID of the user to delete
    :param str current_user_id: The UUID of the admin user performing the deletion
    :return: None
    :raises ObjectDoesNotExist: If the user is not found
    :raises ValidationError: If trying to delete self with public AppTemplates
    """
    try:
        # Check if user is deleting themselves
        is_self_deletion = (user_to_delete.id == current_user.id)

        # Get user's AppTemplates
        public_app_templates = AppTemplates.objects.filter(creator_id=user_to_delete, public=True)
        private_app_templates = AppTemplates.objects.filter(creator_id=user_to_delete, public=False)

        # Self-deletion with public AppTemplate not allowed
        if is_self_deletion and public_app_templates.exists():
            raise ValidationError("Cannot delete your own user while public AppTemplates are assigned to you."
                                  "Delete/Update them first.")

        # Process AppTemplates (releated data is deleted automatically via model cascade)
        private_app_templates.delete()

        # For public AppTemplates, transfer ownership to the current admin performing the deletion
        public_app_templates.update(
            creator_id=current_user,
            updated_at=timezone.now()
        )
        user_to_delete.delete()
    except ValidationError as e:
        raise e

# Currently unused, potential enhancement for the future
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
