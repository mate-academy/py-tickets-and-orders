from django.contrib.auth import get_user_model

from db.models import User


USER = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    new_user = USER.objects.create_user(
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


def get_user(user_id: int) -> User:
    return USER.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user_to_update = USER.objects.get(pk=user_id)

    if username:
        user_to_update.username = username
    if password:
        user_to_update.set_password(password)
    if email:
        user_to_update.email = email
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name

    user_to_update.save()
    return user_to_update
