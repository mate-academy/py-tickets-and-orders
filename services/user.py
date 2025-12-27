from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
) -> User:
    user_data = {"username": username, "password": password}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name
    return get_user_model().objects.create_user(**user_data)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    user.save()
