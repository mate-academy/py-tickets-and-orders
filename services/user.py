from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = User(username=username)

    if first_name:
        user.first_name = first_name
    else:
        user.first_name = ""

    if email:
        user.email = email
    else:
        user.email = ""

    if last_name:
        user.last_name = last_name
    else:
        user.last_name = ""

    with transaction.atomic():
        user.set_password(password)
        user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def get_user_by_username(username: str) -> User:
    return get_user_model().objects.get(username=username)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = get_user_model().objects.get(pk=user_id)

    if username:
        user.username = username

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    with transaction.atomic():
        if password:
            user.set_password(password)

        user.save()
