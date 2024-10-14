from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from eduvmstore.db.models import User

def create_user(id: int, role_id: int) -> User:
    """
    Create a new User entry in the database using Django ORM.
    """
    try:
        new_user = User.objects.create(
            id=id,
            role_id=role_id,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            deleted=False
        )
        return new_user
    except ValidationError as e:
        raise e

def get_user_by_id(id: int) -> User:
    """
    Retrieve a User entry from the database by ID using Django ORM.
    """
    try:
        return User.objects.get(id=id)
    except ObjectDoesNotExist:
        return None
