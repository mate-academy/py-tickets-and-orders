from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        **info,
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **info
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        password: str = None,
        email: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user(user_id)
    if password:
        user.set_password(raw_password=password)
    if email:
        user.email = email
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
