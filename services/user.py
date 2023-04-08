from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    for field_name, value in kwargs.items():
        setattr(new_user, field_name, value)

    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user_model().objects.get(id=user_id)

    for field_name, value in kwargs.items():
        if field_name == "password":
            user.set_password(value)
        else:
            setattr(user, field_name, value)

    user.save()
