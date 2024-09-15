from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> User:

    user = get_user_model().objects.create_user(
        username=username, password=password
    )

    to_set_dict = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for attribute, value in to_set_dict.items():
        if value:
            setattr(user, attribute, value)

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

    to_set_dict = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for attribute, value in to_set_dict.items():
        if value:
            setattr(user, attribute, value)

    if password:
        user.set_password(password)

    user.save()
