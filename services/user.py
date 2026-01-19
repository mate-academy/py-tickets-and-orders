from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404

from db.models import User


def create_user(username: str, password: str,
                email: str = None, first_name: str = None,
                last_name: str = None) -> User:
    try:
        user = User.objects.create_user(username=username, password=password)
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.full_clean()
        user.save()
        return user
    except IntegrityError:
        raise ValueError(f"A user with the username "
                         f"'{username}' already exists.")
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404(f"User with id {user_id} does not exist")


def update_user(user_id: int, username: str = None, password: str = None,
                email: str = None, first_name: str = None,
                last_name: str = None) -> User:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404(f"User with id {user_id} does not exist")
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
    return user
