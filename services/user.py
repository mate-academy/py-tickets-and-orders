import init_django_orm  # noqa: F401

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User
from django.core.exceptions import ValidationError


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> QuerySet:
    user = User.objects.create_user(
        username=username,
        password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user_model().objects.get(id=user_id)
    if username:
        if get_user_model().objects.filter(username=username):
            raise ValidationError(f"User with name {username} already exists. "
                                  f"You should choose another username.")
        user.username = username
    if password:
        user.set_password(password)
    if email:
        if get_user_model().objects.filter(email=email):
            raise ValidationError("User with passed email already exists. "
                                  "You should choose another email.")
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()

    return user
