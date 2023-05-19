from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()
    return new_user


if __name__ == "__main__":
    get_user_model().objects.all()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    user_update = get_user_model().objects.get(id=user_id)
    if username:
        user_update.username = username
    if password:
        user_update.set_password(password)
    if email:
        user_update.email = email
    if first_name:
        user_update.first_name = first_name
    if last_name:
        user_update.last_name = last_name
    user_update.save()
