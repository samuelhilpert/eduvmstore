# app_name/db/models.py
from tokenize import Double

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from .session import Base
from datetime import datetime


class AppTemplate(Base):
    __tablename__ = 'app_template'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, index=True, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)
    short_description = Column(String(255))
    instantiation_notice = Column(String)

    # CRUD info
    creator_id = Column(Integer, ForeignKey('user.id'), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Integer, default=0)

    # version and visibility
    version = Column(String, default="1.0")
    public =Column(Integer, default=0, nullable=False)
    approved = Column(Integer, default=0)

    # resource requirements
    fixed_ram_gb = Column(Float)
    fixed_disk_gb = Column(Float)
    fixed_cores = Column(Integer)
    per_user_ram_gb = Column(Float)
    per_user_disk_gb = Column(Float)
    per_user_cores = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), index=True)

    # CRUD info
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Integer, default=0)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    # for different rights, e.g. 100 for low rights and 4000 for admin rights
    access_level = Column(Integer, nullable=False)


# After defining the model, create the tables:
# Create the tables by running Base.metadata.create_all(bind=engine)