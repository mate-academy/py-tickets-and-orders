from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user_model().objects.create_user(
        username=username, password=password
    )
    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for field, data in user_data.items():
        if data:
            setattr(user, field, data)

    user.save()


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user(user_id)
    user_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for field, data in user_data.items():
        if data:
            setattr(user, field, data)

    if password:
        user.set_password(password)

    user.save()
