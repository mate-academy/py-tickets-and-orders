from db.models import User
from django.db import transaction
from django.contrib.auth.hashers import make_password


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    encrypted_password = make_password(password)

    user = User.objects.create(
        username=username,
        password=encrypted_password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


@transaction.atomic
def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:

    user = User.objects.get(id=user_id)

    if username:
        user.username = username
    if password:
        user.password = make_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    else:
        user.first_name = ""

    if last_name:
        user.last_name = last_name
    else:
        user.last_name = ""

    user.save()

    return user
