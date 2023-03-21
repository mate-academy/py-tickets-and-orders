from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:

    with transaction.atomic():
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
        )
        user.email = email if email is not None else user.email
        user.first_name = first_name if first_name is not None else user.first_name
        user.last_name = last_name if last_name is not None else user.last_name

        return user.save()


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> QuerySet:
    user = get_user_model().objects.get(id=user_id)

    user.username = username if username is not None else user.username
    user.email = email if email is not None else user.email
    user.first_name = first_name if first_name is not None else user.first_name
    user.last_name = last_name if last_name is not None else user.last_name

    if password is not None:
        user.set_password(password)

    return user.save()
