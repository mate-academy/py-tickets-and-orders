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
        username=username)

    if email is not None:
        setattr(user, "email", email)

    if first_name is not None:
        setattr(user, "first_name", first_name)

    if last_name is not None:
        setattr(user, "last_name", last_name)

    user.set_password(password)
    user.save()

    return user


def get_user(user_id: int) -> User:
    user = get_user_model().objects.get(id=user_id)
    return user


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> User:
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
