from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> User:
    user_data = {
        "username": username,
        "password": password,
    }

    user = get_user_model().objects.create_user(**user_data)

    for key, value in kwargs.items():
        if value is not None and value != "":
            setattr(user, key, value)

    user.save()

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user_model().objects.get(id=user_id)

    for key, value in kwargs.items():
        if value is not None and value != "":
            setattr(user, key, value)

    if "password" in kwargs and kwargs["password"]:
        user.set_password(kwargs["password"])

    user.save()
