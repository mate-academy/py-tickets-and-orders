from db.models import User
from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    user_model = get_user_model()

    user = user_model .objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    return user


def get_user(user_id: int) -> User:
    user_model = get_user_model()
    return user_model.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    user_model = get_user(user_id)

    if username:
        user_model.username = username
    if password:
        user_model.set_password(password)
    if email:
        user_model.email = email
    if first_name:
        user_model.first_name = first_name
    if last_name:
        user_model.last_name = last_name

    user_model.save()

    return user_model
