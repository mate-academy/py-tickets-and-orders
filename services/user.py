from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import User


def set_optional_params(
        queryset: User,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    if email:
        queryset.email = email
    if first_name:
        queryset.first_name = first_name
    if last_name:
        queryset.last_name = last_name
    queryset.save()


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    new_user = get_user_model().objects.create_user(username=username)
    new_user.set_password = password,
    set_optional_params(new_user, email, first_name, last_name)
    return new_user


def get_user(user_id: int) -> QuerySet[User]:
    return get_object_or_404(get_user_model(), id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    up_user = get_object_or_404(get_user_model(), id=user_id)
    if username:
        up_user.username = username

    if password:
        up_user.set_password(password)

    set_optional_params(up_user, email, first_name, last_name)
