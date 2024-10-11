import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .session import SessionLocal
from .models import User, Roles, AppTemplate

def create_app_template(db: Session, data: dict):
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

    # Add and commit the new template to the database
    try:
        db.add(new_template)
        db.commit()
        db.refresh(new_template)
        return new_template
    except Exception as e:
        db.rollback()
        raise e


def create_user(id: int, role_id: int):
    """
    Create a new User entry in the database.

    :param id: Unique identifier for the user
    :param role_id: Role ID (foreign key to the Roles model)
    :return: The newly created User object or None if an error occurs
    """

    new_user = User(
        id=id,
        role_id=role_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        deleted=False
    )
    with SessionLocal() as db:
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            db.rollback()
            raise e

# User
def get_user_by_id(id: int):
    """
    Retrieve a User entry from the database by ID.

    :param id: Unique identifier of the user
    :return: The User object if found, else None
    """
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == id).first()
        return user

# Roles
def create_role(name: str, access_level: int) -> Roles:
    """
    Create a new Role entry in the database.

    :param name: The name of the role
    :param access_level: The access level for the role (e.g., 100 for low rights, 4000 for admin rights)
    :return: The newly created Role object or None if an error occurs
    """
    new_role = Roles(
        id=str(uuid.uuid4()),
        name=name,
        access_level=access_level
    )

    with SessionLocal() as db:
        try:
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            return new_role
        except SQLAlchemyError as e:
            db.rollback()
            raise e

def update_role(id: str, name: str = None, access_level: int = None) -> Roles:
    """
    Update an existing Role entry in the database.

    :param id: The unique identifier of the role to update
    :param name: The new name for the role (optional)
    :param access_level: The new access level for the role (optional)
    :return: The updated Role object or None if an error occurs
    """
    with SessionLocal() as db:
        try:
            role = db.query(Roles).filter(Roles.id == id).first()
            if not role:
                raise Exception("Role not found")
                # Exception may need to be adapted to a more specific exception type

            if name is not None:
                role.name = name
            if access_level is not None:
                role.access_level = access_level
            db.commit()
            db.refresh(role)
            return role
        except SQLAlchemyError as e:
            db.rollback()
            raise e
