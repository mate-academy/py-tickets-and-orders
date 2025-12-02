from django.contrib.auth import get_user_model
from typing import Optional
from typing import Any


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None) -> Any:
    user = get_user_model()
    user_data = {"username": username, "password": password}

    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    user = user.objects.create_user(**user_data)
    return user


def get_user(user_id: int) -> Optional[get_user_model()]:
    user_model = get_user_model()

    try:
        return user_model.objects.get(id=user_id)
    except user_model.DoesNotExist:
        return None


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None) -> Optional[get_user_model()]:
    user_model = get_user_model()
    user = get_user(user_id)
    if not user_model:
        return None

    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
