from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> User:
    new_user = get_user_model().objects.create_user(username=username, **kwargs)
    new_user.set_password(password)
    new_user.save()
    return new_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, password: str = None, **kwargs) -> None:
    user = get_user(user_id)
    if password:
        user.set_password(password)
        user.save()
    get_user_model().objects.filter(id=user_id).update(**kwargs)
