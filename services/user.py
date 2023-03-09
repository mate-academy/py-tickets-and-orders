from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str, password: str, **kwargs) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if kwargs.get("email"):
        user.email = kwargs["email"]

    if kwargs.get("first_name"):
        user.first_name = kwargs["first_name"]

    if kwargs.get("last_name"):
        user.last_name = kwargs["last_name"]

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user_model().objects.get(id=user_id)

    for key, value in kwargs.items():

        if key == "password":
            user.set_password(value)
        else:
            user.__setattr__(key, value)

    user.save()
