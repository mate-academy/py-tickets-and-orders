from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email: Optional[str] = "",
                first_name: Optional[str] = "",
                last_name: Optional[str] = "") -> User:
    some_user = get_user_model().objects.create_user(username=username,
                                                     password=password,
                                                     email=email,
                                                     first_name=first_name,
                                                     last_name=last_name)
    return some_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    some_user = get_user_model().objects.get(id=user_id)
    if username:
        some_user.username = username
    if password:
        some_user.set_password(password)
    if email:
        some_user.email = email
    if first_name:
        some_user.first_name = first_name
    if last_name:
        some_user.last_name = last_name
    some_user.save()
