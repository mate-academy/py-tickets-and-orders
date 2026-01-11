from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> None:
    optional_user_data = {}

    if email:
        optional_user_data["email"] = email
    if first_name:
        optional_user_data["first_name"] = first_name
    if last_name:
        optional_user_data["last_name"] = last_name
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **optional_user_data
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    target_user = get_user_model().objects.get(pk=user_id)
    if username:
        target_user.username = username
    if password:
        target_user.set_password(password)
    if email:
        target_user.email = email
    if first_name:
        target_user.first_name = first_name
    if last_name:
        target_user.last_name = last_name

    target_user.save()
