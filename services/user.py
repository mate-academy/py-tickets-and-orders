from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str, password: str, **kwargs) -> None:
    keys = ["email", "first_name", "last_name"]

    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    for key, value in kwargs.items():
        if key in keys:
            user.__setattr__(key, value)
    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                **kwargs) -> None:
    keys = ["username", "email", "first_name", "last_name"]
    user = get_user(user_id)
    for key, value in kwargs.items():
        if key in keys:
            user.__setattr__(key, value)
        elif key == "password":
            user.set_password(value)
    user.save()
