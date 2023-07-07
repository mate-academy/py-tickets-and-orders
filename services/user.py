from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs: dict[str]
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    for el in kwargs:
        if el in ["username", "email", "first_name", "last_name"]:
            setattr(user, el, kwargs[el])

    user.save()
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        **kwargs: dict[str]
) -> None:
    user_update = get_user(user_id)

    for el in kwargs:
        if el in ["username", "email", "first_name", "last_name"]:
            setattr(user_update, el, kwargs[el])
        if el == "password":
            user_update.set_password(kwargs[el])

    user_update.save()
