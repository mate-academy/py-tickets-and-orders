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
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    # Don't want to access DB when I don't need to.
    if not any((username, password, email, first_name, last_name)):
        return

    with transaction.atomic():
        user = get_user_model().objects.get(id=user_id)
        if password:
            user.set_password(password)
        if username:
            user.username = username

        # These fields can be blank, hence `is not None`.
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name

        user.save()
