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
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        new_user.email = email

    if first_name:
        new_user.first_name = first_name

    if last_name:
        new_user.last_name = last_name

    new_user.save()


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
    user_for_update = get_user_model().objects.get(id=user_id)

    if username:
        user_for_update.username = username

    if password:
        user_for_update.set_password(password)

    if email:
        user_for_update.email = email

    if first_name:
        user_for_update.first_name = first_name

    if last_name:
        user_for_update.last_name = last_name

    user_for_update.save()
