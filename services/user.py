from typing import Optional
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> get_user_model():
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> int | None:
    try:
        user = get_user_model().objects.get(pk=user_id)
        return user
    except get_user_model().DoesNotExist:
        return None


def update_user(user_id: int, **kwargs) -> int | None:
    user = get_user(user_id)
    if user:
        for field, value in kwargs.items():
            if field == "username":
                user.username = value
            elif field == "password":
                user.set_password(value)
            elif field == "email":
                user.email = value
            elif field == "first_name":
                user.first_name = value
            elif field == "last_name":
                user.last_name = value
        user.save()
        return user
    else:
        return None
