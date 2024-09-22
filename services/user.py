from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,

) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    for field, value in {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }.items():
        if value:
            setattr(user, field, value)
    user.save()


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
    user = get_user_model().objects.get(id=user_id)

    for field, value in {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }.items():
        if value:
            setattr(user, field, value)

    if password:
        user.set_password(password)
    user.save()
