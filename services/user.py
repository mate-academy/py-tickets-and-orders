from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str = "",
        last_name: str = "",
) -> AbstractUser:
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    user.save()

    return user


def get_user(user_id: int,) -> AbstractUser:

    user = User.objects.get(pk=user_id)
    return user


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> AbstractUser:
    user_model = get_user_model()

    user = user_model.objects.get(pk=user_id)

    if username is not None:
        user.username = username

    if email is not None:
        user.email = email

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if password is not None:
        user.set_password(password)

    user.save()

    return user
