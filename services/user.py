from django.contrib.auth.hashers import make_password
from db.models import User


def create_user(
        username: str,
        password: str,
        user_id: int = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    try:
        user, created = User.objects.update_or_create(
            id=user_id,
            defaults=(
                {"username": username,
                 "password": make_password(password)}
            )
        )
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return user
    except User.DoesNotExist:
        return None


def get_user(user_id: int) -> int:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

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
    return user
