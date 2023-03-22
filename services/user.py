from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    get_user_model().objects.filter(username=username).update(**kwargs)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, password: str = None, **kwargs) -> None:
    user_to_update = get_user(user_id)
    if password:
        user_to_update.set_password(password)
    if kwargs:
        for attribute, value in kwargs.items():
            setattr(user_to_update, attribute, value)

    user_to_update.save()
