from django.contrib.auth import get_user_model
from db.models import User


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    fields_dict = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
    kwargs_dict = {
        param: val for param, val in fields_dict.items() if val is not None
    }
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs_dict
    )
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> User:
    user = get_user(user_id=user_id)
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
    return user
