import uuid
from django.utils import timezone
from django.db.models import Q

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from eduvmstore.db.models import AppTemplates, AppTemplateInstantiationAttributes


def create_app_template(app_template_data: dict):
    """
    Create a new AppTemplate entry in the database using Django ORM.
    The instantiation attributes are also created.

    :param dict app_template_data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    :rtype: AppTemplates
    :raises ValidationError: If any required field is missing or invalid
    """
    if not app_template_data.get('name'):
        raise ValidationError("AppTemplate name cannot be empty")
    if not app_template_data.get('description'):
        raise ValidationError("AppTemplate description cannot be empty")
    if not app_template_data.get('image_id'):
        raise ValidationError("AppTemplate image_id cannot be empty")
    if app_template_data.get('fixed_ram_gb') is None:
        raise ValidationError("AppTemplate fixed_ram_gb cannot be None")
    if app_template_data.get('fixed_disk_gb') is None:
        raise ValidationError("AppTemplate fixed_disk_gb cannot be None")
    if app_template_data.get('fixed_cores') is None:
        raise ValidationError("AppTemplate fixed_cores cannot be None")
    if app_template_data.get('per_user_ram_gb') is None:
        raise ValidationError("AppTemplate per_user_ram_gb cannot be None")
    if app_template_data.get('per_user_disk_gb') is None:
        raise ValidationError("AppTemplate per_user_disk_gb cannot be None")
    if app_template_data.get('per_user_cores') is None:
        raise ValidationError("AppTemplate per_user_cores cannot be None")


    try:
        new_app_template = AppTemplates.objects.create(
            # mandatory fields with [] and optional fields with .get()
            # --> automatic exception raised for mandatory fields
            id=str(uuid.uuid4()),
            name=app_template_data['name'],
            description=app_template_data['description'],
            short_description=app_template_data.get('short_description'),
            instantiation_notice=app_template_data.get('instantiation_notice'),
            script=app_template_data.get('script'),
            image_id=app_template_data['image_id'],
            creator_id=app_template_data['creator_id'],

            # Operational fields
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted_at=None,
            deleted=False,

            # Visibility
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

        # Directly create app_template_instantiation_attributes as they are strongly bound to AppTemplates
        instantiation_attributes = app_template_data.get('instantiation_attributes', [])
        if instantiation_attributes:
            attributes_to_create = [
                AppTemplateInstantiationAttributes(app_template_id=new_app_template,
                                                   name=instantiation_attribute["name"])
                for instantiation_attribute in instantiation_attributes
            ]
            AppTemplateInstantiationAttributes.objects.bulk_create(attributes_to_create)

        return new_app_template
    except ValidationError as e:
        raise e


def list_app_templates() -> list[AppTemplates]:
    """
    Retrieve all AppTemplate records from the database using Django ORM.

    :return: A list of AppTemplate objects
    :rtype: list[AppTemplates]
    """
    return AppTemplates.objects.filter(deleted=False)

def get_app_template_by_id(template_id: str) -> AppTemplates:
    """
    Retrieve a specific AppTemplate by id.

    :param str template_id: The UUID of the AppTemplate
    :return: The AppTemplate object if found
    :rtype: AppTemplates
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    return AppTemplates.objects.get(id=template_id, deleted=False)

def search_app_templates(query: str) -> list[AppTemplates]:
    """
    Search AppTemplate records where fields like name, id, description, etc., match the search string.

    :param str query: The search string
    :return: A list of AppTemplate objects matching the query
    :rtype: list[AppTemplates]
    """
    return AppTemplates.objects.filter(
        Q(name__icontains=query) |
        Q(id__icontains=query) |
        Q(description__icontains=query) |
        Q(short_description__icontains=query) |
        Q(instantiation_notice__icontains=query),
        deleted=False
    )

def get_to_be_approved_app_templates() -> list[AppTemplates]:
    """
    Retrieve AppTemplate records filtered by public and approved fields.

    :return: A list of filtered AppTemplate objects
    :rtype: list[AppTemplates]
    """
    return AppTemplates.objects.filter(public = True , approved = False, deleted=False)

def check_app_template_name_collisions(name: str) -> bool:
    """
    Check if the given AppTemplate name collides with any existing AppTemplate.

    :param str name: The name of the AppTemplate to check
    :return: True if a collision is found, False otherwise
    :rtype: bool
    """
    return AppTemplates.objects.filter(name=name, deleted=False).exists()


def update_app_template(id: str, app_template_data: dict) -> AppTemplates:
    """
    Update an existing AppTemplate record by id.

    :param str id: The UUID of the AppTemplate to update
    :param dict app_template_data: Dictionary containing the updated AppTemplate details
    :return: The updated AppTemplate object
    :rtype: AppTemplates
    :raises ObjectDoesNotExist: If the AppTemplate is not found
    """
    try:
        app_template = AppTemplates.objects.get(id=id, deleted=False)

        # Update fields selectively based on input app_template_data
        for field, value in app_template_data.items():
            setattr(app_template, field, value)

        app_template.updated_at = timezone.now()
        app_template.save()

        return app_template
    except ObjectDoesNotExist as e:
        raise ObjectDoesNotExist("AppTemplate not found")

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
