from typing import Optional

from db.models import User
from django.contrib.auth import get_user_model


def update_or_create_user(
        user: User,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
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


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    new_user = get_user_model()()
    update_or_create_user(
        new_user,
        username,
        password,
        email,
        first_name,
        last_name
    )
    return new_user


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.get(id=user_id)
    update_or_create_user(
        user,
        username,
        password,
        email,
        first_name,
        last_name
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)
