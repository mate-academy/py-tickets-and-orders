from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404


User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    extra_fields = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    extra_fields = {
        key: value for key, value in extra_fields.items() if value is not None
    }

    try:
        User.objects.create_user(
            username=username,
            password=password,
            **extra_fields
        )
    except IntegrityError:
        if email and User.objects.filter(email=email).exists():
            raise ValueError(
                f"A user with the email '{email}' already exists."
            )
        raise ValueError(
            f"A user with the username '{username}' already exists."
        )


def get_user(user_id: int) -> User:
    return get_object_or_404(User, pk=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    user = get_user(user_id)
    extra_fields = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    with transaction.atomic():
        if password:
            user.set_password(password)

        for field, value in extra_fields.items():
            if value is not None:
                setattr(user, field, value)

        user.save()
