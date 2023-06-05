from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> None:

    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                email: Optional[str] = None,
                password: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    user = get_user_model().objects.get(id=user_id)
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
