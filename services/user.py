from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None) -> None:
    user_update = get_user(user_id)

    if username:
        user_update.username = username
    if password:
        user_update.set_password(password)
    if email:
        user_update.email = email
    if first_name:
        user_update.first_name = first_name
    if last_name:
        user_update.last_name = last_name

    user_update.save()
