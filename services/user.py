from django.contrib.auth import get_user_model

import settings


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> settings.AUTH_USER_MODEL:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    if email is not None:
        new_user.email = email

    if first_name is not None:
        new_user.first_name = first_name

    if last_name is not None:
        new_user.last_name = last_name
    new_user.save()

    return new_user


def get_user(user_id: int) -> settings.AUTH_USER_MODEL:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> settings.AUTH_USER_MODEL:
    current_user = get_user(user_id)

    if username is not None:
        current_user.username = username

    if password is not None:
        current_user.set_password(raw_password=password)

    if email is not None:
        current_user.email = email

    if first_name is not None:
        current_user.first_name = first_name

    if last_name is not None:
        current_user.last_name = last_name

    current_user.save()

    return current_user
