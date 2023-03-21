from typing import Optional
from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        email: Optional[str] = None,
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
) -> None:
    user_to_update = get_user(user_id=user_id)

    if username:
        user_to_update.username = username

    if password:
        user_to_update.set_password(password)

    if first_name:
        user_to_update.first_name = first_name

    if last_name:
        user_to_update.last_name = last_name

    if email:
        user_to_update.email = email

    user_to_update.save()
