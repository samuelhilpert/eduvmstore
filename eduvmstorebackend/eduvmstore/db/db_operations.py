from .session import SessionLocal
from .models import User, Roles, AppTemplate

# Create
def create_user(username: str, email: str):
    db = SessionLocal()
    new_user = User(username=username, email=email)
    try:
        db.add(new_user)
        db.commit()  # Commit the transaction
        db.refresh(new_user)  # Refresh the instance to get the updated data
        return new_user
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an error
        print(e)
    finally:
        db.close()

# Get
def get_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()  # Query for the user
    db.close()
    return user

# Update
def update_role_access_level(role_id: int, new_access_level: int):
    db = SessionLocal()
    user = db.query(Roles).filter(Roles.id == role_id).first()
    if user:
        user.access_level = new_access_level  # Update the email
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    db.close()

# Delete
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)  # Delete the user
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(e)
    db.close()

