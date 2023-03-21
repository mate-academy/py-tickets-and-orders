from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:

    creating_user = User.objects.create_user(
        username=username,
        password=password,
    )

    if email:
        creating_user.email = email

    if first_name:
        creating_user.first_name = first_name

    if last_name:
        creating_user.last_name = last_name

    creating_user.save()


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

    updating_user = get_user_model().objects.get(id=user_id)

    if password:
        updating_user.set_password(password)

    if first_name:
        updating_user.first_name = first_name

    if last_name:
        updating_user.last_name = last_name

    if email:
        updating_user.email = email

    if username:
        updating_user.username = username

    updating_user.save()
