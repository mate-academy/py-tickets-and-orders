from django.db import IntegrityError

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        return user
    except IntegrityError:
        raise IntegrityError("A user with this username already exists.")


def get_user(user_id: int) -> User | str:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist."


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None | str:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist."
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
