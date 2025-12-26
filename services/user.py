from django.contrib.auth import get_user_model

from db.models import User

user = get_user_model()


def create_user(username: str, password: str, *, email: str = None,
                first_name: str = None, last_name: str = None) -> None:
    user_data = {key: value for key, value in {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }.items() if value is not None}

    user.objects.create_user(**user_data)


def get_user(user_id: int) -> User:
    return user.objects.get(id=user_id)


def update_user(user_id: int, *,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user_received = get_user(user_id)

    user_data_to_update = {key: value for key, value in {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }.items() if value is not None}

    if user_data_to_update:
        for key, value in user_data_to_update.items():
            setattr(user_received, key, value)

    if password:
        user_received.set_password(password)

    if user_data_to_update or password:
        user_received.save()
