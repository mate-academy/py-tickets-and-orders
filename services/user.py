from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import User

user_ = get_user_model()


def create_user(
        username: str, password: str, email: str | None = None,
        first_name: str | None = None, last_name: str | None = None
) -> User:
    user = user_.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or ""
    )
    return user


def get_user(user_id: int) -> User:
    return user_.objects.get(id=user_id)


@transaction.atomic
def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> None:
    user = user_.objects.get(id=user_id)
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
