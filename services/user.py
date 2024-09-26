from typing import Optional
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User


def set_data(
        user: User,
        username: Optional[str],
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[str] = None
) -> None:
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


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username, password=password)
    set_data(user=user,
             username=username,
             email=email,
             first_name=first_name,
             last_name=last_name)


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.get(id=user_id)
    set_data(user=user,
             username=username,
             password=password,
             email=email,
             first_name=first_name,
             last_name=last_name)
