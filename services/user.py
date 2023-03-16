from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    result_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    if email:
        result_user.email = email

    if first_name:
        result_user.first_name = first_name

    if last_name:
        result_user.last_name = last_name

    return result_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    upd_user = get_user_model().objects.get(id=user_id)

    if username:
        upd_user.username = username
    if password:
        upd_user.set_password(password)
    if email:
        upd_user.email = email
    if first_name:
        upd_user.first_name = first_name
    if last_name:
        upd_user.last_name = last_name

    upd_user.save()

    return upd_user
