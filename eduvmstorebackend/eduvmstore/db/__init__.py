from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from eduvmstorebackend.eduvmstore.db.models import Base

DATABASE_URL = "mysql://your_db_user:your_db_password@localhost:3306/your_db_name"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine) # for db init
