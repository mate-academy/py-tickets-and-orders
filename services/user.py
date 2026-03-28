from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    user_data = {}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    get_user_model().objects.create_user(
        username=username,
        password=password,
        **user_data
    )


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
    current_user = get_user(user_id)

    if username is not None:
        current_user.username = username

    if email is not None:
        current_user.email = email

    if first_name is not None:
        current_user.first_name = first_name

    if last_name is not None:
        current_user.last_name = last_name

    if password is not None:
        current_user.set_password(password)

    current_user.save()
