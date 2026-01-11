from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser


def create_user(
        username: str,
        password: str,
        email: str = None,
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


def get_user(
    user_id: int
) -> AbstractBaseUser:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user_for_update = get_user(user_id)

    if username:
        user_for_update.username = username
    if email:
        user_for_update.email = email
    if first_name:
        user_for_update.first_name = first_name
    if last_name:
        user_for_update.last_name = last_name
    if password:
        user_for_update.set_password(password)

    user_for_update.save()
