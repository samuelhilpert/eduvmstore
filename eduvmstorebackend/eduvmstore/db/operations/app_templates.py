import uuid
from django.utils import timezone
from django.db.models import Q

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from eduvmstore.db.models import AppTemplates


def check_app_template_name_collisions(name: str) -> bool:
    """
    Check if the given AppTemplate name collides with any existing AppTemplate.

    :param str name: The name of the AppTemplate to check
    :return: True if a collision is found, False otherwise
    :rtype: bool
    """
    return AppTemplates.objects.filter(name=name, deleted=False).exists()


def approve_app_template(id: str) -> AppTemplates:
    """
    Update the approved status of an AppTemplate to true.

    :param str id: The UUID of the AppTemplate to approve
    :return: The updated AppTemplate object
    :rtype: AppTemplates
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    try:
        app_template = AppTemplates.objects.get(id=id, deleted=False)
        app_template.approved = True
        app_template.save()
        return app_template
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
