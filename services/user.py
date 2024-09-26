from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None,
                ) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()

    return user


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user_model().objects.get(id=user_id)

    for key, value in kwargs.items():
        if key == "password":
            user.set_password(value)
        else:
            setattr(user, key, value)

    user.save()
