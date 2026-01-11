from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User


def create_user(username: str,
                password: str,
                **extra_fields) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **extra_fields)


def get_user(user_id: int) -> QuerySet:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = User.objects.get(id=user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if email is not None:
        user.email = email
    if username is not None:
        user.first_name = first_name
    if username is not None:
        user.last_name = last_name
    user.save()
