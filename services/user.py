from django.contrib.auth import get_user_model
from typing import Optional


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    user_u = get_user_model()
    user = user_u.objects.create_user(username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> get_user_model:
    user = get_user_model()
    return user.objects.get(pk=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    user_to_update = get_user(user_id)
    if username is not None:
        user_to_update.username = username
    if password is not None:
        user_to_update.set_password(password)
    if email is not None:
        user_to_update.email = email
    if first_name is not None:
        user_to_update.first_name = first_name
    if last_name is not None:
        user_to_update.last_name = last_name
    user_to_update.save()
