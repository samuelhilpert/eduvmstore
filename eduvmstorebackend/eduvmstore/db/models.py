# app_name/db/models.py
from tokenize import Double

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from eduvmstorebackend.eduvmstore.db.session import Base
from datetime import datetime

Base = declarative_base()


class AppTemplate(Base):
    __tablename__ = 'app_template'

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, index=True, foreign_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)
    short_description = Column(String(255))
    instantiation_notice = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    version = Column(String, default="1.0")
    is_public =Column(Integer, default=0, nullable=False)
    fixed_RAM_GB = Column(Double)
    fixed_disk_GB = Column(Double)
    fixed_cores = Column(Integer)
    per_user_RAM_GB = Column(Double)
    per_user_disk_GB = Column(Double)
    per_user_cores = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, index=True, foreign_key=True)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)


# After defining the model, create the tables:
# Create the tables by running Base.metadata.create_all(bind=engine)