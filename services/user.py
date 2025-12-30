from django.contrib.auth import get_user_model
from db.models import User


def create_user(
    username: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
) -> None:

    get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else "",
        email=email if email else "",
    )


def get_user(user_id: int) -> None:
    try:
        user = get_user_model().objects.get(pk=user_id)
    except User.DoesNotExist:
        print("User not found.")
    return user


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    user = get_user(user_id)
    if username:
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
