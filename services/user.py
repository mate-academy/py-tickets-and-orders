from django.contrib.auth import get_user_model
from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = "",
        last_name: str = ""
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name or "",
        last_name=last_name or ""
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    password: str = None,
    username: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    user = User.objects.get(id=user_id)
    if password is not None:
        user.set_password(password)
    for key, value in {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }.items():
        if value is not None:
            setattr(user, key, value)
    user.save()
