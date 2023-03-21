from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )
    return new_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, password: str = None, **kwargs) -> None:
    fields_to_update = kwargs.copy()
    if password:
        fields_to_update["password"] = make_password(password)
    get_user_model().objects.filter(id=user_id).update(**fields_to_update)
