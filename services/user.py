from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional
from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
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
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)