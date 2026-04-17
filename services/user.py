from django.contrib.auth import get_user_model
from typing import Any
from db.models import User

def create_user(username: Any,
                password: Any,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    user = get_user_model().objects.create_user(
        username=username, password=password
    )

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()

    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int,
                username: Any = None,
                password: Any = None,
                email: Any = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user(user_id)

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
