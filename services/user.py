from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = "",
        last_name: str = ""
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    try:
        user = get_user(user_id)
        if username is not None:
            user.username = username
        if password is not None:
            user.password = make_password(password)
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return user
    except ObjectDoesNotExist:
        return None


def get_user(user_id: int) -> User:
    user = get_object_or_404(User, pk=user_id)
    return user
