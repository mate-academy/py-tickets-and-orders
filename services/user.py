from typing import Optional

from django.contrib.auth import get_user_model

from settings import AUTH_USER_MODEL


def create_user(username: str,
                password: str,
                email: Optional[str] = "",
                first_name: Optional[str] = "",
                last_name: Optional[str] = "") -> AUTH_USER_MODEL:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> AUTH_USER_MODEL:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    user = get_user_model().objects.get(id=user_id)
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
