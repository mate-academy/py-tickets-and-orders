from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    User.objects.create_user(
        username=username,
        email=email if email else "",
        password=password,
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else ""
    )


def get_user(user_id: int) -> User:
    try:
        return get_user_model().objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with id {user_id} does not exist")


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
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
