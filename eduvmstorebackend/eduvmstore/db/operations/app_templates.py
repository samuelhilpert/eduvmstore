import re
import logging
from sys import orig_argv

from django.db import transaction
from django.utils import timezone

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from eduvmstore.db.models import AppTemplates

# Pattern to match version suffixes in AppTemplate names.
# This pattern is forbidden as it is automatically used for approved AppTemplates
VERSION_SUFFIX_PATTERN = r'-V\d+$'

def check_current_name_collision(name: str) -> bool:
    """
    Check if the given AppTemplate name collides with any existing AppTemplate.
    or if it has the version suffix reserved for approved AppTemplates.

    :param str name: The name of the AppTemplate to check
    :return: True if a collision is found, False otherwise
    :rtype: bool
    """
    return AppTemplates.objects.filter(name=name, deleted=False).exists()

def has_version_suffix(name: str) -> bool:
    """
    Check if the given AppTemplate name has a version suffix.
    Examples are '-V1', '-V2', etc.

    :param str name: The name of the AppTemplate to check
    :return: True if a version suffix is found, False otherwise
    :rtype: bool
    """
    return bool(re.search(VERSION_SUFFIX_PATTERN, name))


def extract_version_suffix(name: str) -> str:
    """
    Extract the version suffix from an AppTemplate name if present.

    :param str name: The name to check
    :return: The extracted version suffix or empty string if none found
    :rtype: str
    """
    match = re.search(VERSION_SUFFIX_PATTERN, name)
    return match.group(0) if match else ""

@transaction.atomic
def approve_app_template(id: str) -> AppTemplates:
    """
    Approve an AppTemplate by creating a copy with the 'approved' flag set to True.
    The copied AppTemplate name is suffixed with '-V' and the version number to
    ensure unique names.

    :param str id: The UUID of the AppTemplate to approve
    :return: The updated AppTemplate object
    :rtype: AppTemplates
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    try:
        original_app_template = AppTemplates.objects.get(id=id, deleted=False)

        # Create a copy by setting pk to None
        # https://docs.djangoproject.com/en/2.2/topics/db/queries/#copying-model-instances
        public_app_template = AppTemplates.objects.get(id=original_app_template.id, deleted=False)
        public_app_template.pk = None
        public_app_template.name = f"{original_app_template.name}-V{original_app_template.version}"
        public_app_template.approved = True  # Approve the copy
        public_app_template.save()

        # No need for public visibility on original app_template
        # -> no request for approval
        original_app_template.public = False
        original_app_template.version += 1
        original_app_template.save()

        return public_app_template
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"AppTemplate {id} not found.")

@transaction.atomic
def reject_app_template(id: str) -> AppTemplates:
    """
    Update the public and approved status of an AppTemplate to false.

    :param str id: The UUID of the AppTemplate to reject
    :return: The updated AppTemplate object
    :rtype: AppTemplates
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    try:
        app_template = AppTemplates.objects.get(id=id, deleted=False)
        app_template.approved = False
        app_template.public = False
        app_template.save()
        return app_template
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"AppTemplate {id} not found.")

# Currently unused, potential enhancement for the future
@transaction.atomic
def soft_delete_app_template(id: str) -> None:
    """
    Soft delete an AppTemplate record by setting the 'deleted' flag and 'deleted_at' timestamp.

    :param str id: The UUID of the AppTemplate to delete
    :return: None
    :rtype: None
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    try:
        template = AppTemplates.objects.get(id=id, deleted=False)
        template.deleted = True
        template.deleted_at = timezone.now()
        template.updated_at = template.deleted_at
        template.save()
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"AppTemplate {id} not found.")
