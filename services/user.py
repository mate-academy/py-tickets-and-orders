from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
    )
    user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()

    return user


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    update_user = get_user_model().objects.update_user(id=user_id)
    if username:
        update_user.username = username
    if password:
        update_user.set_password(password)
    if email:
        update_user.email = email
    if first_name:
        update_user.first_name = first_name
    if last_name:
        update_user.last_name = last_name

    update_user.save()
