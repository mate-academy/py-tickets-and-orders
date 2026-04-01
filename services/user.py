from typing import Optional
from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise ValueError(f"User with id {user_id} does not exist")

    if username and username != user.username:
        if (
            get_user_model()
            .objects
            .filter(username=username)
            .exclude(pk=user_id)
            .exists()
        ):
            raise ValueError(f"Username {username} is already taken")
        user.username = username

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
