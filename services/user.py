from django.contrib.auth import get_user_model

import settings


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if any([email, first_name, last_name]):
        update_user(
            user_id=user.id,
            email=email,
            first_name=first_name,
            last_name=last_name
        )


def get_user(user_id: int) -> settings.AUTH_USER_MODEL:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
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

    user.save()
