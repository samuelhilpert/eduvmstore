import uuid

from django.contrib.postgres.aggregates import BoolOr
from django.utils import timezone
from django.db.models import Q

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from eduvmstore.db.models import AppTemplate

def create_app_template(app_template_data: dict):
    """
    Create a new AppTemplate entry in the database using Django ORM.

    :param app_template_data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    """
    try:
        new_app_template = AppTemplate.objects.create(
            id=str(uuid.uuid4()),
            name=app_template_data['name'],
            description=app_template_data['description'],
            short_description=app_template_data.get('short_description'),
            instantiation_notice=app_template_data.get('instantiation_notice'),
            image_id=app_template_data['image_id'],
            creator_id=app_template_data['creator_id'],

            # Operational fields
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted_at=None,
            deleted=False,

            # Version and visibility
            version=app_template_data.get('version', '1.0'),
            public=app_template_data.get('public', False),
            approved=app_template_data.get('approved', False),

            # Resource requirements
            fixed_ram_gb=app_template_data['fixed_ram_gb'],
            fixed_disk_gb=app_template_data['fixed_disk_gb'],
            fixed_cores=app_template_data['fixed_cores'],
            per_user_ram_gb=app_template_data['per_user_ram_gb'],
            per_user_disk_gb=app_template_data['per_user_disk_gb'],
            per_user_cores=app_template_data['per_user_cores']
        )
        return new_app_template
    except ValidationError as e:
        raise e


def list_app_templates() -> list[AppTemplate]:
    """
    Retrieve all AppTemplate records from the database using Django ORM.

    :return: A list of AppTemplate objects
    """
    return AppTemplate.objects.filter(deleted=False)

def get_app_template_by_id(template_id: str) -> AppTemplate:
    """
    Retrieve a specific AppTemplate by id.

    :param template_id: The UUID of the AppTemplate
    :return: The AppTemplate object if found, else raises DoesNotExist
    """
    return AppTemplate.objects.get(id=template_id, deleted=False)

def search_app_templates(query: str) -> list[AppTemplate]:
    """
    Search AppTemplate records where fields like name, id, description, etc., match the search string.

    :param query: The search string
    :return: A list of AppTemplate objects matching the query
    """
    return AppTemplate.objects.filter(
        Q(name__icontains=query) |
        Q(id__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query) |
        Q(instantiation_notice__icontains=query) |
        Q(version__icontains=query),
        # Q(creator__name__icontains=query), # image name is also missing need to check first if this works??
        deleted=False
    )

def get_to_be_approved_app_templates() -> list[AppTemplate]:
    """
    Retrieve AppTemplate records filtered by public and approved fields.

    :return: A list of filtered AppTemplate objects
    """
    return AppTemplate.objects.filter(public = True , approved = False, deleted=False)

def check_app_template_name_collisions(name: str) -> bool:
    """
    Check if the given AppTemplate name collides with any existing AppTemplate.

    :param name: The name of the AppTemplate to check
    :return: True if a collision is found, False otherwise
    """
    return AppTemplate.objects.filter(name=name, deleted=False).exists()


def update_app_template(id: str, data: dict) -> AppTemplate:
    """
    Update an existing AppTemplate record by id.

    :param id: The UUID of the AppTemplate to update
    :param data: Dictionary containing the updated AppTemplate details
    :return: The updated AppTemplate object
    """
    try:
        app_template = AppTemplate.objects.get(id=id, deleted=False)

        # Update fields selectively based on input data
        for field, value in data.items():
            setattr(app_template, field, value)

        app_template.updated_at = timezone.now()
        app_template.save()

        return app_template
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("AppTemplate not found")

def approve_app_template(id: str) -> AppTemplate:
    """
    Update the approved status of an AppTemplate to true.

    :param id: The UUID of the AppTemplate to approve
    :return: The updated AppTemplate object
    """
    try:
        template = AppTemplate.objects.get(id=id, deleted=False)
        template.approved = True
        template.save()
        return template
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("AppTemplate not found.")


def soft_delete_app_template(id: str) -> None:
    """
    Soft delete an AppTemplate record by setting the 'deleted' flag and 'deleted_at' timestamp.

    :param id: The UUID of the AppTemplate to delete
    """
    try:
        template = AppTemplate.objects.get(id=id, deleted=False)
        template.deleted = True
        template.deleted_at = timezone.now()
        template.updated_at = template.deleted_at
        template.save()
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("AppTemplate not found.")


