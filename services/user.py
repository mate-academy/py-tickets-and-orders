from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str, password: str, email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:

    user = get_user_model().objects.create_user(
        username=username, password=password,
        email=email if email else "",
        first_name=first_name if first_name
        else "", last_name=last_name if last_name
        else "")

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int, username: str = None, password: str = None,
                email: str = None,
                first_name: str = None, last_name: str = None) -> User:

    selected_user = get_user(user_id)

    if username is not None:
        selected_user.username = username

    if password is not None:
        selected_user.set_password(password)

    if email is not None:
        selected_user.email = email

    if first_name is not None:
        selected_user.first_name = first_name

    if last_name is not None:
        selected_user.last_name = last_name

    selected_user.save()

    return selected_user
