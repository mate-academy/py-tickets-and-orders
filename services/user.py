from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()
    return new_user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> None:
    user_to_upd = get_user_model().objects.get(id=user_id)

    if username is not None:
        user_to_upd.username = username
    if password:
        user_to_upd.set_password(password)
    if email:
        user_to_upd.email = email
    if first_name:
        user_to_upd.first_name = first_name
    if last_name:
        user_to_upd.last_name = last_name

    user_to_upd.save()
