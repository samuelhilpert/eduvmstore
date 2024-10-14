import uuid
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from eduvmstore.db.models import AppTemplate

def create_app_template(app_template_data: dict):
    """
    Create a new AppTemplate entry in the database using Django ORM.

    :param app_template_data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    """
    try:
        # Using Django's ORM to create a new AppTemplate instance
        new_template = AppTemplate.objects.create(
            id=str(uuid.uuid4()),  # Generate unique UUID
            name=app_template_data['name'],
            description=app_template_data['description'],
            short_description=app_template_data.get('short_description'),
            instantiation_notice=app_template_data.get('instantiation_notice'),
            image_id=app_template_data['image_id'],
            creator_id=app_template_data['creator_id'],

            # The fields below are managed by Django automatically
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted_at=None,
            deleted=False,

            # Version and visibility
            version=app_template_data.get('version', '1.0'),
            public=app_template_data.get('public', False),
            approved=app_template_data.get('approved', False),

            # Resource requirements
            fixed_ram_gb=app_template_data.get('fixed_ram_gb', 0),
            fixed_disk_gb=app_template_data.get('fixed_disk_gb', 0),
            fixed_cores=app_template_data.get('fixed_cores', 0),
            per_user_ram_gb=app_template_data.get('per_user_ram_gb', 0),
            per_user_disk_gb=app_template_data.get('per_user_disk_gb', 0),
            per_user_cores=app_template_data.get('per_user_cores', 0)
        )
        return new_template
    except ValidationError as e:
        # Handle validation errors from the Django ORM model
        raise e


def list_app_templates() -> list[AppTemplate]:
    """
    Retrieve all AppTemplate records from the database using Django ORM.

    :return: A list of AppTemplate objects
    """
    return AppTemplate.objects.all()  # Use Django ORM's objects manager to list all templates
