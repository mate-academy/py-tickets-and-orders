from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import User


@transaction.atomic
def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int | User) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int | User,
                username: str | None = None,
                password: str | None = None,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
