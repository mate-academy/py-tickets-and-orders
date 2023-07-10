from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs,
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> [User, str]:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        **kwargs
) -> [None, str]:
    user = get_user(user_id=user_id)

    if "username" in kwargs:
        user.username = kwargs["username"]

    if "password" in kwargs:
        user.set_password(raw_password=kwargs["password"])

    if "email" in kwargs:
        user.email = kwargs["email"]

    if "first_name" in kwargs:
        user.first_name = kwargs["first_name"]

    if "last_name" in kwargs:
        user.last_name = kwargs["last_name"]

    user.save()
