from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        password: str,
        username: str,
        email: str = "",
        first_name: str = "",
        last_name: str = "",
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)
    if username:
        user.username = username
    if email is not None:
        user.email = email or ""
    if first_name is not None:
        user.first_name = first_name or ""
    if last_name is not None:
        user.last_name = last_name or ""

    user.save()
