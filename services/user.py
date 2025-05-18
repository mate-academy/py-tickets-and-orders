from django.contrib.auth import get_user_model
from typing import Optional, Any


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> Any:
    users = get_user_model()

    user_data = {
        "username" : username,
        "password" : password
    }

    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    user = users.objects.create_user(**user_data)

    return user


def get_user(user_id: int) -> Any:
    user = get_user_model().objects.get(pk=user_id)
    return user


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> Any:

    user = get_user_model().objects.get(pk=user_id)

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

    return user
