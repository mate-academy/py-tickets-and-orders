from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        user.email = email

    user.save()
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None
) -> User:
    user = get_user(user_id=user_id)
    for attr_name, attr_value in {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }.items():
        if attr_value is not None:
            setattr(user, attr_name, attr_value)
    if password is not None:
        user.set_password(password)

    user.save()
    return user
