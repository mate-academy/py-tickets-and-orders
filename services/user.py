from django.contrib.auth import get_user_model
from settings import AUTH_USER_MODEL


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> AUTH_USER_MODEL:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> AUTH_USER_MODEL:
    user = get_user_model().objects.get(id=user_id)
    return user


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> AUTH_USER_MODEL:
    user = get_user(user_id=user_id)
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
