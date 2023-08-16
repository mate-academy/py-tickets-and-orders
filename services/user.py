from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    **kwargs
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    for attr_name, attr_value in kwargs.items():
        if attr_value:
            setattr(user, attr_name, attr_value)

    user.save()

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    **kwargs,
) -> None:
    user = get_user_model().objects.get(id=user_id)

    for attr_name, attr_value in kwargs.items():
        if attr_name == "password":
            user.set_password(attr_value)
        else:
            setattr(user, attr_name, attr_value)

    user.save()
