from db.models import User
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:

    currently_user = get_user_model().objects.get(id=user_id)

    if username:
        currently_user.username = username
    if password:
        currently_user.set_password(password)
    if email:
        currently_user.email = email
    if first_name:
        currently_user.first_name = first_name
    if last_name:
        currently_user.last_name = last_name

    currently_user.save()
