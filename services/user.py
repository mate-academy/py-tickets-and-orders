from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str | None = "",
        first_name: str | None = "",
        last_name: str | None = ""
) -> User:
    return get_user_model().objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    ).set_password(password)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None
) -> None:
    user = get_user(user_id)

    for key, value in locals().items():
        if key != "user_id":
            if value:
                if key == "password":
                    user.set_password(value)
                else:
                    setattr(user, key, value)
    user.save()
