from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(username: str, password: str, **kwargs: Any) -> AbstractUser:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    for field, value in kwargs.items():
        setattr(user, field, value)
    user.save()
    return user


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs: Any) -> AbstractUser:
    user = get_user(user_id)
    password: Optional[str] = kwargs.pop("password", None)
    for field, value in kwargs.items():
        setattr(user, field, value)
    if password:
        user.set_password(password)
    user.save()
    return user
