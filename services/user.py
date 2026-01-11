from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:

    user = get_user_model().objects.create_user(
        username=username, password=password
    )

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    up_user = get_user_model().objects.get(id=user_id)
    if username is not None:
        up_user.username = username
    if password is not None:
        up_user.set_password(password)
    if email is not None:
        up_user.email = email
    if first_name is not None:
        up_user.first_name = first_name
    if last_name is not None:
        up_user.last_name = last_name
    up_user.save()
