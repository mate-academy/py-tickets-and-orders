from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    kwargs: dict = {"username": username, "password": password}
    if email is not None:
        kwargs["email"] = email
    if first_name is not None:
        kwargs["first_name"] = first_name
    if last_name is not None:
        kwargs["last_name"] = last_name
    return User.objects.create_user(**kwargs)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if password is not None:
        user.set_password(password)
    user.save()
    return user
