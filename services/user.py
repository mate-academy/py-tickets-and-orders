from sqlite3 import IntegrityError

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None):
    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError:
        raise ValidationError("Username already exists")

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()


def get_user(user_id: int):
    user = User.objects.get(id=user_id)
    return user


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = User.objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
