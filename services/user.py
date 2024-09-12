from django.contrib.auth import get_user_model

from db.models import User


def set_data(
        user: User,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        username: str = None,
        password: str = None
) -> None:
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if username:
        user.username = username
    if password:
        user.set_password(password)
    user.save()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    set_data(user, email, first_name, last_name)


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
    user_to_update = get_user(user_id)
    set_data(user_to_update, email, first_name, last_name, username, password)
