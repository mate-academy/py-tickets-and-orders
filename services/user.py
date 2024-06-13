from typing import Any

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    optional_attributes = [
        ("email", email),
        ("first_name", first_name),
        ("last_name", last_name)
    ]
    set_user_attributes(user, optional_attributes)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    user = get_user_model().objects.get(pk=user_id)

    if password:
        user.set_password(password)

    optional_attributes = [
        ("username", username),
        ("email", email),
        ("first_name", first_name),
        ("last_name", last_name)
    ]
    set_user_attributes(user, optional_attributes)


def set_user_attributes(user: User, attributes: list[tuple[str, Any]]) -> None:
    [setattr(user, key, value) for key, value in attributes if value]
    user.save()
