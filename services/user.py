from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


@transaction.atomic
def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user_kwargs = {"username": username, "password": password}
    if email:
        user_kwargs["email"] = email
    if first_name:
        user_kwargs["first_name"] = first_name
    if last_name:
        user_kwargs["last_name"] = last_name

    return User.objects.create_user(**user_kwargs)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


@transaction.atomic
def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
    return user
