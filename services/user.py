from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def check_user_values(
    user: User,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> None:
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


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    check_user_values(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user.save()

    return user


def get_user(user_id: int) -> User:
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
    check_user_values(
        user=user,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user.save()
