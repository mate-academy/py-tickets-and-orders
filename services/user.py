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
    get_user_id = get_user_model().objects.get(id=user_id)
    if username:
        get_user_id.username = username
    if password:
        get_user_id.set_password(password)
    if email:
        get_user_id.email = email
    if first_name:
        get_user_id.first_name = first_name
    if last_name:
        get_user_id.last_name = last_name
    get_user_id.save()
