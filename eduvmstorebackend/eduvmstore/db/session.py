from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings
from sqlalchemy.ext.declarative import declarative_base
import os

# Get the absolute path to the database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../db.sqlite3')

engine = create_engine(f'sqlite:///{DATABASE_PATH}', connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()