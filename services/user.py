from typing import Optional
from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:

        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    arguments = locals()
    user = get_user(arguments.pop("user_id"))

    if password:
        user.set_password(arguments.pop("password"))

    for user_field, value in arguments.items():
        if value:
            setattr(user, user_field, value)
    user.save()


def get_user_by_username(username: str) -> User:
    return get_user_model().objects.get(username=username)
