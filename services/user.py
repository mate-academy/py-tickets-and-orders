from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None
) -> None:
    new_user = get_user_model().objects.create_user(
        username=username, password=password
    )

    if first_name:
        new_user.first_name = first_name

    if last_name:
        new_user.last_name = last_name

    if email:
        new_user.email = email

    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[str] = None
) -> None:
    select_user = get_user(user_id=user_id)

    if username:
        select_user.username = username

    if email:
        select_user.email = email

    if first_name:
        select_user.first_name = first_name

    if last_name:
        select_user.last_name = last_name

    if password:
        select_user.set_password(password)

    select_user.save()
