from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from .session import Base
from datetime import datetime


class AppTemplate(Base):
    __tablename__ = 'app_template'

    id = Column(String(36), primary_key=True, index=True)
    image_id = Column(String(36), index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)
    short_description = Column(String(255))
    instantiation_notice = Column(String)

    # CRUD info
    creator_id = Column(String(36), ForeignKey('user.id'), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Boolean, default=False)

    # version and visibility
    version = Column(String, default="1.0")
    public =Column(Boolean, default=False, nullable=False)
    approved = Column(Boolean, default=False)

    # resource requirements
    fixed_ram_gb = Column(Float)
    fixed_disk_gb = Column(Float)
    fixed_cores = Column(Integer)
    per_user_ram_gb = Column(Float)
    per_user_disk_gb = Column(Float)
    per_user_cores = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    id = Column(String(36), primary_key=True, index=True)
    role_id = Column(String(36), ForeignKey('roles.id'), index=True)

    # CRUD info
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    deleted = Column(Boolean, default=False)


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)

    # for different rights, e.g. 100 for low rights and 4000 for admin rights
    access_level = Column(Integer, nullable=False)


# After defining the model, create the tables:
# Create the tables by running Base.metadata.create_all(bind=engine)