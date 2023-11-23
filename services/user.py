from typing import Any

from django.contrib.auth import get_user_model


def create_user(
    username: str,
    password: Any,
    email: str = None,
    first_name: str = "",
    last_name: str = "",
) -> get_user_model():
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: Any = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> get_user_model():
    user = get_user_model()
    user = user.objects.get(id=user_id)

    if user:
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
