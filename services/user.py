from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str,
        password: Any,
        email: Any = "",
        first_name: str = "",
        last_name: str = ""
) -> None:

    User.objects.create_user(
        username,
        email,
        password,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Any = None,
        password: Any = None,
        email: Any = None,
        first_name: str = None,
        last_name: str = None

) -> User:
    user = User.objects.get(id=user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user
