from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
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
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> None:
    user = get_user(user_id=user_id)

    user.username = username if username else user.username
    user.set_password(password) if password else user.password
    user.email = email if email else user.email
    user.first_name = first_name if first_name else user.first_name
    user.last_name = last_name if last_name else user.last_name

    user.save()
