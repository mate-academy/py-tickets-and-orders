from typing import Optional

from django.contrib.auth import get_user_model

from db.models import User


def update_user_information(
        user: User,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    if email is not None:
        user.email = email

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name


def create_user(
        username: str, password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    update_user_information(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user.save()

    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    user = User.objects.get(id=user_id)

    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)

    update_user_information(
        user=user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user.save()

    return user
