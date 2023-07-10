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

    for user_data in kwargs:
        if user_data in ["username", "email", "first_name", "last_name"]:
            setattr(user, user_data, kwargs[user_data])

    user.save()
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        **kwargs: dict[str]
) -> None:
    user_update = get_user(user_id)

    for user_data in kwargs:
        if user_data in ["username", "email", "first_name", "last_name"]:
            setattr(user_update, user_data, kwargs[user_data])
        if user_data == "password":
            user_update.set_password(kwargs[user_data])

    user_update.save()
