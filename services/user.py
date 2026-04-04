from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def get_user(*, user_id: int) -> models.Model:
    return User.objects.get(id=user_id)


def create_user(
    username: str,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> models.Model:
    user = User.objects.create_user(
        username=username,
        password=password
    )

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    if password:
        user.set_password(password)

    user.save()
    return user


def update_user(
    user_id: int,
    **kwargs
) -> models.Model:
    user = get_user(user_id=user_id)

    for field in ["username", "password", "email", "first_name", "last_name"]:
        if field in kwargs and kwargs[field] is not None:
            if field == "password":
                user.set_password(kwargs[field])

            else:
                setattr(user, field, kwargs[field])

    user.save()
    return user
