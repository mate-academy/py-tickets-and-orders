from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user_model().objects.create_user(
        username=username, password=password
    )

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()

    return user


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

    user = get_user_model().objects.filter(id=user_id)
    if username:
        user.update(username=username)
    if email:
        user.update(email=email)
    if first_name:
        user.update(first_name=first_name)
    if last_name:
        user.update(last_name=last_name)
    if password:
        user = get_user_model().objects.get(id=user_id)
        user.set_password(password)
        user.save()
