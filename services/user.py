from typing import Optional

from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or ""
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> User:
    user = get_user(user_id=user_id)

    if password:
        user.set_password(password)

    user_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }

    for field, value in user_data.items():
        if value:
            setattr(user, field, value)

    user.save()

    return user
