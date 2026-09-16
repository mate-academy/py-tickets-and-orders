from typing import Any

from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None
                ) -> None:
    new_user = get_user_model().objects.create_user(
        username=username, password=password
    )
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name
    new_user.save()


def get_user(user_id: int) -> Any:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: str | None = None,
                password: str | None = None,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None
                ) -> User:
    user_get = get_user_model().objects.get(id=user_id)

    if username:
        user_get.username = username
    if password:
        user_get.set_password(password)
    if email:
        user_get.email = email
    if first_name:
        user_get.first_name = first_name
    if last_name:
        user_get.last_name = last_name
    user_get.save()
    return user_get
