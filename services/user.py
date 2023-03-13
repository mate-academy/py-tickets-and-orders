from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> QuerySet:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def get_user(user_id: int) -> User | None:
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

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
    return user
