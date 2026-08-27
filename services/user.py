from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    data_to_update = (
        ("username", username),
        ("email", email),
        ("first_name", first_name),
        ("last_name", last_name),
    )
    user = get_user(user_id)

    if password:
        user.set_password(password)

    for key, value in data_to_update:
        if value:
            setattr(user, key, value)

    user.save()

    return user
