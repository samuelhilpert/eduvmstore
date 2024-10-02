# app_name/db/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class AppTemplate(Base):
    __tablename__ = 'app_templates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    image = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# After defining the model, create the tables:
# Create the tables by running Base.metadata.create_all(bind=engine)
