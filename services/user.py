from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email if email else "",
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else ""
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    user = get_user_model().objects.get(pk=user_id)
    if password:
        user.set_password(password)

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
