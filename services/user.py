from typing import Optional
from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    extra_fields = {}
    if email is not None:
        extra_fields["email"] = email
    if first_name is not None:
        extra_fields["first_name"] = first_name
    if last_name is not None:
        extra_fields["last_name"] = last_name

    return User.objects.create_user(
        username=username,
        password=password,
        **extra_fields,
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
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
