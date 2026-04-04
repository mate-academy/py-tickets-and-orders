from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(
        username: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
) -> None:
    new_user = User.objects.create_user(
        username=username,
        password=password,
    )

    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name
    if email:
        new_user.email = email

    new_user.save()


def get_user(user_id: int) -> User:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError(f"User with ID {user_id} does not exist.")

    return user


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
) -> None:
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValueError(f"User with ID {user_id} does not exist.")

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        try:
            validate_email(email)
            user.email = email
        except ValidationError:
            raise ValueError("Invalid email format")

    user.save()
    return user
