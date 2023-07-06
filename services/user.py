from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                password: str = None,
                **kwargs) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)

    for data_field, data in kwargs.items():
        setattr(user, data_field, data)

    user.save()
