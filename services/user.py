from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> AbstractUser:
    optional_fields = {}
    if email:
        optional_fields["email"] = email
    if first_name:
        optional_fields["first_name"] = first_name
    if last_name:
        optional_fields["last_name"] = last_name
    created_user = get_user_model().objects.create_user(
        username=username,
        password=password,
        **optional_fields
    )
    return created_user


def get_user(user_id: int) -> AbstractUser:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> AbstractUser:
    updated_user = get_user(user_id)
    if username:
        updated_user.username = username
    if password:
        updated_user.set_password(password)
    if email:
        updated_user.email = email
    if first_name:
        updated_user.first_name = first_name
    if last_name:
        updated_user.last_name = last_name
    updated_user.save()
    return updated_user
