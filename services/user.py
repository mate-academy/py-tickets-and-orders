from django.contrib.auth import get_user_model
from db.models import User


def create_user(username: str, password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    current_user = get_user(user_id)

    if username:
        current_user.username = username
    if password:
        current_user.set_password(password)
    if email:
        current_user.email = email
    if first_name:
        current_user.first_name = first_name
    if last_name:
        current_user.last_name = last_name

    current_user.save()
