import re
from django.utils import timezone

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from eduvmstore.db.models import AppTemplates


def check_app_template_name_collisions(name: str) -> bool:
    """
    Check if the given AppTemplate name collides with any existing AppTemplate.
    or if it has the version suffix reserved for approved AppTemplates.

    :param str name: The name of the AppTemplate to check
    :return: True if a collision is found, False otherwise
    :rtype: bool
    """

    if has_version_suffix(name):
        return True

    return AppTemplates.objects.filter(name=name, deleted=False).exists()

def has_version_suffix(name: str) -> bool:
    """
    Check if the given AppTemplate name has a version suffix.
    Examples are '-V1', '-V2', etc.

    :param str name: The name of the AppTemplate to check
    :return: True if a version suffix is found, False otherwise
    :rtype: bool
    """
    return re.search(r'-V\d+$', name)

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
        public_app_template.name = original_app_template.name + "-V" +str(original_app_template.version)
        public_app_template.approved = True  # Approve the copy
        public_app_template.save()


        # No need for public visibility on original app_template
        # -> no request for approval
        original_app_template.public = False
        original_app_template.version += 1
        original_app_template.save()

        return public_app_template
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("AppTemplate not found.")

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
        raise ObjectDoesNotExist("AppTemplate %s not found.", id)

# Currently unused, potential enhancement for the future
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
        raise ObjectDoesNotExist("AppTemplate not found.")
