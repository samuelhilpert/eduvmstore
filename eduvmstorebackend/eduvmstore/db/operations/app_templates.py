import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from eduvmstore.db.session import SessionLocal
from eduvmstore.db.models import AppTemplate

def create_app_template(app_template_data: dict):
    """
    Create a new AppTemplate entry in the database.

    :param db: SQLAlchemy database session
    :param app_template_data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    """

    # Create a new AppTemplate instance
    new_template = AppTemplate(
        id=str(uuid.uuid4()),  # Generate unique UUID
        name=app_template_data['name'],
        description=app_template_data['description'],
        short_description=app_template_data['short_description'],
        instantiation_notice=app_template_data.get('instantiation_notice'),  # Optional
        image_id=app_template_data['image_id'],
        creator_id=app_template_data['creator_id'],

        # CRUD info
        created_at=datetime.utcnow(),
        updated_at=None,
        deleted_at=None,
        deleted=False,

        # Version and visibility
        version=app_template_data.get('version', '1.0'),
        public=app_template_data.get('public', False),
        approved=app_template_data.get('approved', False),

        # Resource requirements
        fixed_ram_gb=app_template_data['fixed_ram_gb'],  # Optional
        fixed_disk_gb=app_template_data['fixed_disk_gb'],  # Optional
        fixed_cores=app_template_data['fixed_cores'],  # Optional
        per_user_ram_gb=app_template_data['per_user_ram_gb'],  # Optional
        per_user_disk_gb=app_template_data['per_user_disk_gb'],  # Optional
        per_user_cores=app_template_data['per_user_cores']  # Optional
    )

    with SessionLocal() as db:
        try:
            db.add(new_template)
            db.commit()
            db.refresh(new_template)
            return new_template
        except SQLAlchemyError as e:
            db.rollback()
            raise e

def list_app_templates() -> list[AppTemplate]:
    """
    Retrieve all AppTemplate records from the database.

    :return: A list of AppTemplate objects
    """
    with SessionLocal() as db:
        return db.query(AppTemplate).all()