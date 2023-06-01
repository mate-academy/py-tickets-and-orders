from typing import Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User


def add_extra_information(
        instance: User,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
) -> None:
    if email:
        instance.email = email
    if first_name:
        instance.first_name = first_name
    if last_name:
        instance.last_name = last_name
    if username:
        instance.username = username
    if password:
        instance.set_password(password)
    instance.save()


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> QuerySet:
    new_user = get_user_model().objects.create_user(
        username=username, password=password
    )
    add_extra_information(
        new_user, email=email, first_name=first_name, last_name=last_name
    )
    return new_user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> QuerySet:
    user = User.objects.get(id=user_id)
    add_extra_information(
        user,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user
