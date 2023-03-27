from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    data_check(user, email, first_name, last_name)

    user.save()


def get_user(
        user_id: int
) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:

    user = get_user(user_id)

    if username:
        user.username = username
    if password:
        user.set_password(password)

    data_check(user, email, first_name, last_name)

    user.save()


def data_check(user_model: QuerySet,
               email: Optional[str] = None,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None) -> None:
    if email:
        user_model.email = email

    if first_name:
        user_model.first_name = first_name

    if last_name:
        user_model.last_name = last_name
