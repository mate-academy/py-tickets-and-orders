from typing import Any
from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_user(
        username: str,
        password: int,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> QuerySet:
    user = get_user_model()

    user = user.objects.create_user(
        username=username,
        password=password,
    )

    if email is not None:
        user.email = email

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> Any | None:
    user = get_user_model()

    try:
        user = user.objects.get(id=user_id)
        return user
    except user.DoesNotExist:
        return None


def update_user(
        user_id: int,
        username: str = None,
        password: int = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model()

    try:
        user = user.objects.get(id=user_id)

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
    except user.DoesNotExist:
        return None
