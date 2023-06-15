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
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    optional_fields = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    set_optional_attribute(optional_fields=optional_fields, user=user)
    return user


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
    user = get_user(user_id=user_id)
    optional_fields = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    set_optional_attribute(optional_fields=optional_fields, user=user)


def set_optional_attribute(optional_fields: dict, user: User) -> None:
    for field, value in optional_fields.items():
        if value is not None:
            if field == "password":
                user.set_password(value)
            else:
                setattr(user, field, value)
    user.save()
