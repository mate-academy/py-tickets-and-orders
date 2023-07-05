from django.contrib.auth import get_user_model
from db.models import User


def create_user(username: str, password: str, **kwargs) -> None:
    default_kwargs = {
        "email": "",
        "first_name": "",
        "last_name": ""
    }
    kwargs = {**default_kwargs, **kwargs}

    get_user_model().objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user(user_id)

    fields_to_update = ["username", "password", "email", "first_name",
                        "last_name"]

    for field in fields_to_update:
        if field in kwargs:
            value = kwargs[field]
            if field == "password":
                user.set_password(value)
            else:
                setattr(user, field, value)

    user.save()
