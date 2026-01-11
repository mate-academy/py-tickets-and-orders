from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:

    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if email is not None:
        new_user.email = email

    if first_name is not None:
        new_user.first_name = first_name

    if last_name is not None:
        new_user.last_name = last_name

    new_user.save()

    return new_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> None:
    updating_user = get_user_model().objects.get(id=user_id)

    if username is not None:
        updating_user.username = username

    if password is not None:
        updating_user.set_password(password)

    if email is not None:
        updating_user.email = email

    if first_name is not None:
        updating_user.first_name = first_name

    if last_name is not None:
        updating_user.last_name = last_name

    updating_user.save()
