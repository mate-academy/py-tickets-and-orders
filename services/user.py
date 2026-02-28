from typing import Any
from django.contrib.auth import get_user_model


def get_user(user_id: int) -> Any:
    return get_user_model().objects.get(id=user_id)


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> Any:
    user_model = get_user_model()
    return user_model.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> Any:
    # Reusing get_user function for better maintainability
    user = get_user(user_id)

    if username:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
