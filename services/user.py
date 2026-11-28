from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    user_data = {
        "username": username,
        "password": password,
    }

    if email is not None:
        user_data["email"] = email
    if first_name is not None:
        user_data["first_name"] = first_name
    if last_name is not None:
        user_data["last_name"] = last_name

    get_user_model().objects.create_user(**user_data)


def get_user(
        user_id: int
) -> AbstractUser:
    user = get_user_model().objects.get(pk=user_id)
    return user


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    user = get_user(user_id)

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
