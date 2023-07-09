from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from db.models import User


def set_user_values(
    user: User,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    if email:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("this value mast be validated!")
        else:
            user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    user = User.objects.create_user(
        username=username,
        password=password
    )

    set_user_values(user, email, first_name, last_name)

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def get_user_by_username(username: str) -> User:
    return get_user_model().objects.get(username=username)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    user = get_user(user_id)

    if username:
        user.username = username

    if password:
        user.set_password(password)

    set_user_values(user, email, first_name, last_name)

    user.save()
