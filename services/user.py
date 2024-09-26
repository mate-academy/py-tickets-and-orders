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
        **kwargs
    )
    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    updated_user = get_user_model().objects.get(id=user_id)

    for field, value in kwargs.items():
        if field == "password":
            updated_user.set_password(value)
        else:
            setattr(updated_user, field, value)

    updated_user.save()
