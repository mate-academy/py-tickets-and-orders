from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist

from db.models import User


def create_user(username: str, password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    user = get_user_model().objects.create_user(
        username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> AbstractBaseUser | None:
    try:
        return get_user_model().objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
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
