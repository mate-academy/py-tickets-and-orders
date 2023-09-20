from django.contrib.auth import get_user_model

from db.models import User as UserType

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> UserType:
    user = User.objects.create_user(  # type: ignore
        username=username, password=password
    )

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> UserType:
    return User.objects.get(id=user_id)  # type: ignore


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> UserType:
    user = get_user(user_id)

    if username:
        user.username = username  # type: ignore

    if password:
        user.set_password(password)

    if email:
        user.email = email  # type: ignore

    if first_name:
        user.first_name = first_name  # type: ignore

    if last_name:
        user.last_name = last_name  # type: ignore

    user.save()
    return user
