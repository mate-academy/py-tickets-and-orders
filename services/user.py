from django.contrib.auth import get_user_model
from db.models import User
from typing import Optional


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if email is not None:
        user.email = email
        user.save()
    if last_name is not None:
        user.last_name = last_name
        user.save()
    if first_name is not None:
        user.first_name = first_name
        user.save()


def get_user(user_id: int) -> User:
    user = User.objects.all()
    return user.get(pk=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    user = User.objects.get(pk=user_id)
    if username is not None:
        user.username = username
        user.save()
    if password is not None:
        user.password = password
        user.save()
    if email is not None:
        user.email = email
        user.save()
    if first_name is not None:
        user.first_name = first_name
        user.save()
    if last_name is not None:
        user.last_name = last_name
        user.save()
    if password is not None:
        user.set_password(password)
        user.save()
