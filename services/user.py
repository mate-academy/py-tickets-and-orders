from django.contrib.auth import get_user_model

import init_django_orm  # noqa: F401
from db.models import User


def create_user(username: str,
                password: str,
                first_name: str = None,
                last_name: str = None,
                email: str = None,
                ) -> User:
    new_user = User.objects.create_user(username=username,
                                        password=password)
    if email is not None:
        new_user.email = email
    if first_name is not None:
        new_user.first_name = first_name
    if last_name is not None:
        new_user.last_name = last_name
    new_user.save()
    return new_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    user = get_user_model().objects.get(pk=user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
