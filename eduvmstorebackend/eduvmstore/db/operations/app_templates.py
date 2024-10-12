import uuid
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from eduvmstorebackend.eduvmstore.db.session import SessionLocal
from eduvmstorebackend.eduvmstore.db.models import User, Roles, AppTemplate

def create_app_template(data: dict):
    """
    Create a new AppTemplate entry in the database.

    :param db: SQLAlchemy database session
    :param data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    """

    # Create a new AppTemplate instance
    new_template = AppTemplate(
        id=str(uuid.uuid4()),  # Generate unique UUID
        name=data['name'],
        description=data.get('description'),  # Optional
        short_description=data.get('short_description'),  # Optional
        instantiation_notice=data.get('instantiation_notice'),  # Optional
        image_id=data['image_id'],
        creator_id=data['creator_id'],

        # CRUD info
        created_at=datetime.utcnow(),
        updated_at=None,
        deleted_at=None,
        deleted=False,

        # Version and visibility
        version=data.get('version', '1.0'),
        public=data.get('public', False),
        approved=data.get('approved', False),

        # Resource requirements
        fixed_ram_gb=data.get('fixed_ram_gb'),  # Optional
        fixed_disk_gb=data.get('fixed_disk_gb'),  # Optional
        fixed_cores=data.get('fixed_cores'),  # Optional
        per_user_ram_gb=data.get('per_user_ram_gb'),  # Optional
        per_user_disk_gb=data.get('per_user_disk_gb'),  # Optional
        per_user_cores=data.get('per_user_cores')  # Optional
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