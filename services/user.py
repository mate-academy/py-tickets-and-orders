from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(
    user_id: int | None = None, username: str | None = None
) -> User:
    if username:
        return get_user_model().objects.get(username=username)
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user_to_update = get_user(user_id)

    if username:
        user_to_update.username = username

    if password:
        user_to_update.set_password(password)

    if email:
        user_to_update.email = email

    if first_name:
        user_to_update.first_name = first_name

    if last_name:
        user_to_update.last_name = last_name

    user_to_update.save()

    return user_to_update
