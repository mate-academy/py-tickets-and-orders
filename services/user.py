from django.core.exceptions import ObjectDoesNotExist, ValidationError

from db.models import User
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValueError(f"User with ID {user_id} does not exist.")


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    try:
        user = get_user(user_id)
    except ValueError as e:
        raise e

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

    try:
        user.save()
    except ValidationError as e:
        raise ValueError(f"Error updating user: {e}")

    return user
