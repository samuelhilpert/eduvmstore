import uuid

from sqlalchemy.exc import SQLAlchemyError

from eduvmstorebackend.eduvmstore.db.session import SessionLocal
from eduvmstorebackend.eduvmstore.db.models import Roles


def create_role(data: dict) -> Roles:
    """
    Create a new Role entry in the database.

    :param name: The name of the role
    :param access_level: The access level for the role (e.g., 100 for low rights, 4000 for admin rights)
    :return: The newly created Role object or None if an error occurs
    """
    new_role = Roles(
        id=str(uuid.uuid4()),
        name=data['name'],
        access_level=data['access_level']
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
