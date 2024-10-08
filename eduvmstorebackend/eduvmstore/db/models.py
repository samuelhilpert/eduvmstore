# app_name/db/models.py
from tokenize import Double

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from eduvmstorebackend.eduvmstore.db.session import Base
from datetime import datetime


class AppTemplate(Base):
    __tablename__ = 'app_template'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, index=True, foreign_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)
    short_description = Column(String(255))
    instantiation_notice = Column(String)
    creator_id = Column(Integer, index=True, foreign_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Integer, default=0)
    version = Column(String, default="1.0")
    public =Column(Integer, default=0, nullable=False)
    approved = Column(Integer, default=0)
    fixed_ram_gb = Column(Double)
    fixed_disk_gb = Column(Double)
    fixed_cores = Column(Integer)
    per_user_ram_gb = Column(Double)
    per_user_disk_gb = Column(Double)
    per_user_cores = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, index=True, foreign_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Integer, default=0)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    access_level = Column(Integer, nullable=False)


# After defining the model, create the tables:
# Create the tables by running Base.metadata.create_all(bind=engine)