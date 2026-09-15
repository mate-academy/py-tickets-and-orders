from django.contrib.auth import get_user_model
from django.db import transaction


@transaction.atomic
def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> get_user_model():
    extra_fields = {}
    if email is not None:
        extra_fields["email"] = email
    if first_name is not None:
        extra_fields["first_name"] = first_name
    if last_name is not None:
        extra_fields["last_name"] = last_name

    return get_user_model().objects.create_user(
        username=username,
        password=password,
        **extra_fields
    )


def get_user(
    user_id: int
) -> get_user_model():
    return get_user_model().objects.get(pk=user_id)


@transaction.atomic
def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> get_user_model():
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
    return user
