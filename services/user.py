from django.db import transaction
from django.contrib.auth import get_user_model
from typing import Any


def get_user(user_id: int) -> Any:
    user_model = get_user_model()
    return user_model.objects.get(pk=user_id)


@transaction.atomic
def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> Any:
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or ""
    )
    return user


@transaction.atomic
def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> Any:
    user = get_user(user_id)

    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    user.first_name = first_name if first_name is not None else ""
    user.last_name = last_name if last_name is not None else ""

    user.save()
    return user
