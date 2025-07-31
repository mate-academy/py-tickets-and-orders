from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> Optional[AbstractBaseUser]:
    user_model = get_user_model()
    return user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name or "",
        last_name=last_name or "",
    )


def get_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
) -> AbstractBaseUser:
    user_model = get_user_model()
    filters = {}
    if user_id:
        filters["pk"] = user_id
    if username:
        filters["username"] = username
    if password:
        filters["password"] = password
    if email:
        filters["email"] = email
    if first_name:
        filters["first_name"] = first_name

    return user_model.objects.get(**filters)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)
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
