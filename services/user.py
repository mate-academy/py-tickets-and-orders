from typing import Optional

from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    new_user = User.objects.create_user(
        username=username,
        password=password
    )

    user_info = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for name, value in user_info.items():
        if value:
            setattr(new_user, name, value)

    new_user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = User.objects.get(id=user_id)

    data_to_update = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    if password:
        user.set_password(raw_password=password)

    for name, value in data_to_update.items():
        if value:
            setattr(user, name, value)

    user.save()
