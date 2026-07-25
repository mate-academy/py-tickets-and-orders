from django.contrib.auth import get_user_model
from typing import Any


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> Any:
    user_model = get_user_model()
    kwargs = {}
    if email:
        kwargs["email"] = email
    if first_name:
        kwargs["first_name"] = first_name
    if last_name:
        kwargs["last_name"] = last_name
    return user_model.objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int = None, username: str = None) -> Any:
    user_model = get_user_model()
    if username:
        return user_model.objects.get(username=username)
    return user_model.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> Any:
    user = get_user(user_id=user_id)

    for key, value in kwargs.items():
        if key == "password":
            user.set_password(value)
        else:
            setattr(user, key, value)

    user.save()
    return user
