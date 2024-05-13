from db.models import User
from typing import Optional
from django.contrib.auth import get_user_model
from typing import Any


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else ""
    )
    return user


def get_user(user_id: int) -> User:
    user = User.objects.get(id=user_id)
    return user


def update_user(user_id: int, **kwargs: Any) -> get_user_model():
    user = get_user_model().objects.get(id=user_id)
    for key, value in kwargs.items():
        if key == "password":
            user.set_password(value)
        else:
            setattr(user, key, value)
    user.save()
    return user
