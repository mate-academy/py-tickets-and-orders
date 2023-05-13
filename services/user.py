from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def check_optional_parameters_and_set(
        user: QuerySet,
        email: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str]
) -> None:
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
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    check_optional_parameters_and_set(
        new_user, email, first_name, last_name
    )


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> None:
    up_user = get_user_model().objects.get(id=user_id)

    if username:
        up_user.username = username

    if password:
        up_user.set_password(password)

    check_optional_parameters_and_set(
        up_user, email, first_name, last_name
    )
