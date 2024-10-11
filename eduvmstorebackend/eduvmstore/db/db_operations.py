from .session import SessionLocal
from .models import User, Roles, AppTemplate
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

# Create
def create_app_template(db: Session, data: dict):
    """
    Create a new AppTemplate entry in the database.

    :param db: SQLAlchemy database session
    :param data: Dictionary containing the AppTemplate details
    :return: The newly created AppTemplate object
    """

    # Create a new AppTemplate instance
    new_template = AppTemplate(
        id=str(uuid.uuid4()),  # Generate a unique UUID for the id
        name=data['name'],
        description=data.get('description'),  # Optional field
        short_description=data.get('short_description'),  # Optional field
        instantiation_notice=data.get('instantiation_notice'),  # Optional field
        image_id=data['image_id'],
        creator_id=data['creator_id'],  # Foreign key to User model

        # CRUD info
        created_at=datetime.utcnow(),  # Automatically set to current timestamp
        updated_at=None,  # Default to None (will be set during updates)
        deleted_at=None,  # Default to None (will be set when deleted)
        deleted=False,  # Default to False

        # Version and visibility
        version=data.get('version', '1.0'),  # Default to '1.0'
        public=data.get('public', False),  # Default to False
        approved=data.get('approved', False),  # Default to False

        # Resource requirements
        fixed_ram_gb=data.get('fixed_ram_gb'),  # Optional
        fixed_disk_gb=data.get('fixed_disk_gb'),  # Optional
        fixed_cores=data.get('fixed_cores'),  # Optional
        per_user_ram_gb=data.get('per_user_ram_gb'),  # Optional
        per_user_disk_gb=data.get('per_user_disk_gb'),  # Optional
        per_user_cores=data.get('per_user_cores')  # Optional
    )

    # Add and commit the new template to the database
    try:
        db.add(new_template)
        db.commit()
        db.refresh(new_template)  # Get the latest state of the new object
        return new_template
    except Exception as e:
        db.rollback()  # Roll back in case of error
        raise e  # Raise the exception to be handled at a higher level


def create_user(id: int, role_id: int):
    db = SessionLocal()
    new_user = User(
        id=id,
        role_id=role_id,
        created_at=datetime.utcnow(),  # Automatically set the created_at field
        updated_at=datetime.utcnow(),  # Automatically set the updated_at field
        deleted=False  # Set the deleted field to False by default
    )
    try:
        db.add(new_user)
        db.commit()  # Commit the transaction
        db.refresh(new_user)  # Refresh the instance to get the updated data
        return new_user
    except SQLAlchemyError as e:
        db.rollback()  # Roll back the transaction in case of an error
        print(f"Error occurred: {e}")
        return None
    finally:
        db.close()

# Get
def get_user_by_id(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()  # Query for the user
    db.close()
    return user
