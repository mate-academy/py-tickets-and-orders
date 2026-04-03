from typing import Optional

from django.db.models import QuerySet

from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = "",
    first_name: Optional[str] = "",
    last_name: Optional[str] = "",
) -> QuerySet:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()
    return user


def get_user(user_id: int) -> QuerySet:
    user = User.objects.get(id=user_id)
    return user


def update_user(user_id: int, **kwargs) -> QuerySet:
    user = User.objects.get(id=user_id)
    if "username" in kwargs:
        user.username = kwargs["username"]
    if "password" in kwargs:
        user.set_password(kwargs["password"])
    if "email" in kwargs:
        user.email = kwargs["email"]
    if "first_name" in kwargs:
        user.first_name = kwargs["first_name"]
    if "last_name" in kwargs:
        user.last_name = kwargs["last_name"]
    user.save()
    return user
