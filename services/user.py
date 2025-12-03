from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    optional = {
        field: value for field, value in locals().items()
        if field not in ("username", "password") and value is not None
    }
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **optional
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    optional, user = locals(), get_user(user_id=user_id)
    for field, value in optional.items():
        if field == "password" and value is not None:
            user.set_password(value)
            continue
        if field != "user_id" and value is not None:
            setattr(user, field, value)

    user.save()
