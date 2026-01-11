from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = "",
    last_name: str = ""
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return new_user


def get_user(user_id: int) -> User:
    try:
        return get_user_model().objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError(f"There is no user with id '{user_id}'")


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> User:
    user = get_user(user_id)

    if username:
        user.username = username

    if password:
        user.set_password(password)

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.full_clean()
    user.save()
    return user
