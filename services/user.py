from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:

    email = email or ""
    first_name = first_name or ""
    last_name = last_name or ""

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> QuerySet:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user_model().objects.get(id=user_id)

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email

    user.first_name = first_name \
        if first_name is not None else (user.first_name or "")

    user.last_name = last_name \
        if last_name is not None else (user.last_name or "")

    if password is not None:
        user.set_password(password)

    user.save()
    return user
