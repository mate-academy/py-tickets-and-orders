from django.db.models import QuerySet
from django.contrib.auth import get_user_model


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
    set_user_fields(
        user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def set_user_fields(
        user: get_user_model(),
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model().objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    set_user_fields(
        user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
