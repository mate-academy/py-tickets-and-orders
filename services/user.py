from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model()
    user = user.objects.create_user(username, email, password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    user = get_user_model()
    return user.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model()
    user = user.objects.get(id=user_id)
    input_values = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    for param, value in input_values.items():
        if value:
            user.__setattr__(param, value)
    if password:
        user.set_password(password)
    user.save()
