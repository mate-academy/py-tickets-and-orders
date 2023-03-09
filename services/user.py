from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


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

    arguments = ["username", "password", "email", "first_name", "last_name"]
    for argument in arguments:
        if locals()[argument]:
            if argument == "password":
                user.set_password(locals()[argument])
            else:
                setattr(user, argument, locals()[argument])
    user.save()
