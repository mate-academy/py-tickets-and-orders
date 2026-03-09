from django.contrib.auth import get_user_model
from typing import Optional


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> Optional[User]:
    kwargs = {"username": username, "password": password}

    if email is not None:
        kwargs["email"] = email

    if first_name is not None:
        kwargs["first_name"] = first_name

    if last_name is not None:
        kwargs["last_name"] = last_name

    user = get_user_model().objects.create_user(**kwargs)
    return user


def get_user(user_id: int) -> User | None:
    return get_user_model().objects.filter(pk=user_id).first()


def update_user(user_id: int, **user_data) -> User:
    user = get_user(user_id)

    if user is None:
        return

    password = user_data.pop("password", None)
    for field in ("username", "email", "first_name", "last_name"):
        if field in user_data:
            setattr(user, field, user_data[field])

    if password is not None:
        user.set_password(password)

    user.save()

    return user
