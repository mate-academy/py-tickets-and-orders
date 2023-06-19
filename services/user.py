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

    if email:
        new_user.email = email

    if first_name:
        new_user.first_name = first_name

    if last_name:
        new_user.last_name = last_name

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
    user_to_update = get_user(user_id)

    attributes = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    for attribute, value in attributes.items():
        if value:
            setattr(user_to_update, attribute, value)

    user_to_update.save()
