from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> User:
    users_info = {
        "username": username,
        "password": password
    }
    if email:
        users_info["email"] = email
    if first_name:
        users_info["first_name"] = first_name
    if last_name:
        users_info["last_name"] = last_name
    created_user = get_user_model().objects.create_user(**users_info)
    return created_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> User:
    updated_user = get_user(user_id)
    if username:
        updated_user.username = username
    if password:
        updated_user.set_password(password)
    if email:
        updated_user.email = email
    if first_name:
        updated_user.first_name = first_name
    if last_name:
        updated_user.last_name = last_name
    updated_user.save()
    return updated_user
