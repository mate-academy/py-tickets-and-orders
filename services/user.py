from django.contrib.auth import get_user_model

from settings import AUTH_USER_MODEL


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    for attr, value in kwargs.items():
        if attr in ["email", "first_name", "last_name"]:
            setattr(user, attr, value)
    user.save()


def get_user(user_id: int) -> AUTH_USER_MODEL:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        password: str = None,
        **kwargs
) -> None:
    user = get_user_model().objects.get(id=user_id)
    if password:
        user.set_password(password)

    for attr, value in kwargs.items():
        if attr in ["email", "first_name", "last_name", "username"]:
            setattr(user, attr, value)
    user.save()
