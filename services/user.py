from django.contrib.auth import get_user_model

from db.models import User
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        new_user.email = email
        # new_user.save()
    if first_name:
        new_user.first_name = first_name
        # new_user.save()
    if last_name:
        new_user.last_name = last_name

    new_user.save()

    return new_user


def get_user(user_id: User) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: User,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:

    user_upd = User.objects.get(id=user_id)
    if username:
        user_upd.username = username
    if email:
        user_upd.email = email
    if first_name:
        user_upd.first_name = first_name
    if last_name:
        user_upd.last_name = last_name
    user_upd.save()

    if password:
        user_psswd = User.objects.get(id=user_id)
        user_psswd.set_password(password)
        user_psswd.save()
