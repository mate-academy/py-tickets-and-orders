from typing import Optional
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: str = "",
    last_name: str = "",
) -> User:
    """
    Create a new user with required fields.
    """
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> Optional[User]:
    """
    Get user by ID or return None if not found.
    """
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Optional[User]:
    """
    Update user details.
    """
    user = get_user(user_id)
    if not user:
        return None

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user
