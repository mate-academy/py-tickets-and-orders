from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def update_user_fields(
        user: User,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    update_user_fields(user, **kwargs)
    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs
) -> None:
    updated_user = get_user_model().objects.get(id=user_id)
    if username:
        updated_user.username = username
    if password:
        updated_user.set_password(password)
    update_user_fields(updated_user, **kwargs)
    updated_user.save()
