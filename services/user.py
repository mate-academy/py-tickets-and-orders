from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> User | None:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int, **kwargs) -> User | None:
    user = get_user(user_id)

    if not user:
        return None

    for field, value in kwargs.items():
        if field == "password":
            user.set_password(value)
        else:
            setattr(user, field, value)

    user.save()
    return user
