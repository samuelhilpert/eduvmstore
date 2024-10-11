# create_tables.py
from .session import engine, Base  # Adjust import based on your structure
from .models import AppTemplate, User, Roles  # Adjust based on your structure

# Create the tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")