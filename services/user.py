from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> AbstractUser:
    if email:
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email format")

    user_data = {
        "username": username,
        "password": password,
    }

    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    user = get_user_model().objects.create_user(**user_data)

    return user


def get_user(user_id: int) -> AbstractUser:
    try:
        return get_user_model().objects.get(pk=user_id)
    except get_user_model().DoesNotExist:
        raise ValueError(f"User with id {user_id} does not exist")


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> AbstractUser:
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


def get_user_by_username(username: str) -> AbstractUser:
    return get_user_model().objects.get(username=username)


def delete_user(user_id: int) -> None:
    user = get_user(user_id)
    user.delete()


def user_exists(username: str) -> bool:
    return get_user_model().objects.filter(username=username).exists()
