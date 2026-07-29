from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> User:
    optional_parameters = {}
    if email:
        optional_parameters["email"] = email

    if first_name:
        optional_parameters["first_name"] = first_name

    if last_name:
        optional_parameters["last_name"] = last_name

    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        **optional_parameters
    )

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


@transaction.atomic
def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
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
