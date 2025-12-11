from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(
        username: str,
        password: str,
        email: str | None = "",
        first_name: str | None = "",
        last_name: str | None = "") -> AbstractUser:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        email=email,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if password:
        user.set_password(password)
    user.save()
