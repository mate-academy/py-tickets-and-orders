from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    extra_attributes = {}
    if email:
        extra_attributes["email"] = email
    if first_name:
        extra_attributes["first_name"] = first_name
    if last_name:
        extra_attributes["last_name"] = last_name
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        **extra_attributes
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


@transaction.atomic
def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    extra_attributes = {}
    if username:
        extra_attributes["username"] = username
    if email:
        extra_attributes["email"] = email
    if first_name:
        extra_attributes["first_name"] = first_name
    if last_name:
        extra_attributes["last_name"] = last_name
    user = get_user(user_id)
    if password:
        user.set_password(password)

    for name, value in extra_attributes.items():
        setattr(user, name, value)

    user.save()
    return user
