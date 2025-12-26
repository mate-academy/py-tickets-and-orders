from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
if TYPE_CHECKING:
    from db.models import User as UserType


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> "UserType":
    extras = {}
    if email is not None:
        extras["email"] = email
    if first_name is not None:
        extras["first_name"] = first_name
    if last_name is not None:
        extras["last_name"] = last_name

    user = get_user_model().objects.create_user(
        username=username,
        password=password,  # буде захешовано
        **extras,
    )
    return user


def get_user(user_id: int) -> "UserType":
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
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
