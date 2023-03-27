from typing import Optional
from django.contrib.auth import get_user_model
from db.models import User


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> None:
    current_user = {"username": username, "password": password}
    if email is not None:
        current_user["email"] = email
    if first_name is not None:
        current_user["first_name"] = first_name
    if last_name is not None:
        current_user["last_name"] = last_name

    get_user_model().objects.create_user(**current_user)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user: User = get_user_model()
    current_user = user.objects.filter(id=user_id)

    if username is not None:
        current_user.update(username=username)
    if password is not None:
        current_user_for_password = get_user(user_id)
        current_user_for_password.set_password(password)
        current_user_for_password.save()
    if email is not None:
        current_user.update(email=email)
    if first_name is not None:
        current_user.update(first_name=first_name)
    if last_name is not None:
        current_user.update(last_name=last_name)
