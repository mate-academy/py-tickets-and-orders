from typing import Optional

from django.contrib.auth import get_user_model
from db.models import User


def create_user(username: str, password: str, **kwargs) -> None:
    default_kwargs = {
        "email": "",
        "first_name": "",
        "last_name": ""
    }
    kwargs = {**default_kwargs, **kwargs}

    get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                password: Optional[str] = None,
                **kwargs) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)

    fields_to_update = [
        "username", "email", "first_name", "last_name"
    ]
    for key, value in kwargs.items():
        if key in fields_to_update:
            setattr(user, key, value)
    user.save()
