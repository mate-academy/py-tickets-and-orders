from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> AbstractUser:
    user_data = {}

    if email is not None:
        user_data["email"] = email
    if first_name is not None:
        user_data["first_name"] = first_name
    if last_name is not None:
        user_data["last_name"] = last_name

    return get_user_model().objects.create_user(
        username=username,
        password=password,
        **user_data,
    )


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(pk=user_id)


def get_user_by_username(username: str) -> AbstractUser:
    return get_user_model().objects.get(username=username)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> AbstractUser:
    user = get_user(user_id=user_id)

    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user
