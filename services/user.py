from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    fields = ["username", "email", "first_name", "last_name"]
    for data_field, data in kwargs.items():
        if data and (data_field in fields):
            setattr(user, data_field, data)

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                password: str = None,
                **kwargs) -> None:
    user = get_user(user_id)

    fields = ["username", "email", "first_name", "last_name"]
    for data_field, data in kwargs.items():
        if data and (data_field in fields):
            setattr(user, data_field, data)

    if password:
        user.set_password(password)

    user.save()
