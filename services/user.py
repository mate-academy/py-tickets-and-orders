from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    fields = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        **{name: value for name, value in fields.items() if value is not None},
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    user = get_user(user_id)
    fields = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
    for name, value in fields.items():
        if value is not None:
            setattr(user, name, value)
    if password is not None:
        user.set_password(password)
    user.save()
    return user
