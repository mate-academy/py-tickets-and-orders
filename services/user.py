from django.contrib.auth import get_user_model

from db.models import User


VALID_USER_ATTRIBUTES = ['email', 'first_name', 'last_name']


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
        if attr in VALID_USER_ATTRIBUTES:
            setattr(user, attr, value)
    user.save()


def get_user(user_id: int) -> User:
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
        if attr in VALID_USER_ATTRIBUTES:
            setattr(user, attr, value)
    user.save()
