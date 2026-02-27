from typing import Optional
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    """
    Create a new user with encrypted password and optional fields.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def get_user(user_id: int) -> User:
    """
    Retrieve a user by their ID.
    """
    user_model = get_user_model()
    try:
        return user_model.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValueError(f"User with ID {user_id} does not exist.")


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    """
    Update user details, encrypting the password if provided.
    """
    user = get_user(user_id)
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
