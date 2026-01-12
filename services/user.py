from typing import Optional

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = "",
    last_name: Optional[str] = "",
) -> None:
    User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
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
) -> None:
    up_user = get_user(user_id=user_id)

    if username:
        up_user.username = username

    if password:
        up_user.set_password(password)

    if email:
        up_user.email = email

    if first_name:
        up_user.first_name = first_name

    if last_name:
        up_user.last_name = last_name

    up_user.save()
