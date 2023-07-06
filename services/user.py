from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    user = get_user_model().objects.create_user(
        username=username, password=password
    )
    for field, data in kwargs.items():
        if data:
            setattr(user, field, data)

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                password: str = None,
                **kwargs) -> None:
    user = get_user(user_id)

    for field, data in kwargs.items():
        if data:
            setattr(user, field, data)

    if password:
        user.set_password(password)

    user.save()
