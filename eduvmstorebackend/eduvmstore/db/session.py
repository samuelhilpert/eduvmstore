from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings


engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session object
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()