from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser


def create_user(
    *,
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> AbstractBaseUser:
    user_model = get_user_model()
    user = user_model.objects.create_user(username=username, password=password)

    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user


def get_user(*, user_id: int) -> AbstractBaseUser:
    user_model = get_user_model()
    return user_model.objects.get(id=user_id)


def update_user(
    *,
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> AbstractBaseUser:
    user = get_user(user_id=user_id)

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if password is not None:
        user.set_password(password)

    user.save()
    return user
