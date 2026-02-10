from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    upd_user = get_user(user_id)

    if username is not None:
        upd_user.username = username

    if password is not None:
        upd_user.set_password(password)

    if email is not None:
        upd_user.email = email

    if first_name is not None:
        upd_user.first_name = first_name

    if last_name is not None:
        upd_user.last_name = last_name

    upd_user.save()
