from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> AbstractUser:
    user_data = {"username": username, "password": password}
    for field, value in {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }.items():
        if value is not None:
            user_data[field] = value
    return get_user_model().objects.create_user(**user_data)


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> AbstractUser:
    user = get_user(user_id)
    for field, value in {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }.items():
        if value is not None:
            setattr(user, field, value)
    if password is not None:
        user.set_password(password)
    user.save()
    return user
