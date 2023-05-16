from typing import Optional

from django.contrib.auth import models

from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
):
    user = User.objects.create_user(
        username=username,
        password=password
    )

    if email:
        user.email.set(email)
    if first_name:
        user.first_name.set(first_name)
    if last_name:
        user.last_name.set(last_name)
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    user = User.objects.get(id=user_id)

    for arg in locals().keys():
        if arg != "id" and arg != "password" and locals()[arg] is not None:
            user[arg] = locals()[arg]
        if password:
            user.set_password(password)
    user.save()
