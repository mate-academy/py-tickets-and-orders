from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> AbstractUser:
    if email:
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email")

    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> bool:
    changed = False

    user = get_user(user_id=user_id)

    if username:
        user.username = username

    if password:
        user.set_password(password)

    if email:
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email")
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    if username or password or email or first_name or last_name:
        user.save()
        changed = True

    return changed
