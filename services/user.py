from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:

    tmp_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    if email:
        tmp_user.email = email
    if first_name:
        tmp_user.first_name = first_name
    if last_name:
        tmp_user.last_name = last_name

    tmp_user.save()

    return tmp_user


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

    tmp_user = get_user(user_id)

    if username:
        tmp_user.username = username
    if password:
        tmp_user.set_password(password)
    if email:
        tmp_user.email = email
    if first_name:
        tmp_user.first_name = first_name
    if last_name:
        tmp_user.last_name = last_name

    tmp_user.save()
