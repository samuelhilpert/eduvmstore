import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from eduvmstorebackend.eduvmstore.db.session import SessionLocal
from eduvmstorebackend.eduvmstore.db.models import User

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
