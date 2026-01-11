from django.core.exceptions import ObjectDoesNotExist

from db.models import User
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    new_user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    if first_name is not None:
        new_user.first_name = first_name
    if last_name is not None:
        new_user.last_name = last_name
    new_user.save()
    return new_user


def get_user(user_id: int) -> Optional[User]:
    try:
        user = User.objects.get(pk=user_id)
        return user
    except ObjectDoesNotExist:
        return None


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    user = get_user(user_id)
    if user is None:
        raise AttributeError(f"User with id {user_id} does not exist")
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
    return user
