from django.contrib.auth import get_user_model

from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> get_user_model():
    user = get_user_model()
    kwargs = {}
    if email is not None:
        kwargs["email"] = email
    if first_name is not None:
        kwargs["first_name"] = first_name
    if last_name is not None:
        kwargs["last_name"] = last_name
    return user.objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> get_user_model():
    user = get_user_model()
    return user.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user_model()
    user = user.objects.get(id=user_id)
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
