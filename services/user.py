from db.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = "",

):
    return get_user_model().objects.create(
        username=username,
        password=make_password(password),
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int):
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        password: str = None,
        **kwargs
):

    user = get_user(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)

    if password:
        user.set_password(password)

    user.save()
