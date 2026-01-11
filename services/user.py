from django.contrib.auth import get_user_model
from db.models import User
from django.db.models import QuerySet


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None,
                *args,
                **kwargs) -> User:
    user = get_user_model().objects.create_user(
        username=username, *args, **kwargs
    )

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
    return get_user_model().objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> QuerySet:
    user = get_user_model().objects.filter(id=user_id)

    if password is not None:
        user_for_update = get_user_model().objects.get(id=user_id)
        user_for_update.set_password(password)
        user_for_update.save()

    to_update = {}

    if username is not None:
        to_update["username"] = username

    if email is not None:
        to_update["email"] = email

    if first_name is not None:
        to_update["first_name"] = first_name

    if last_name is not None:
        to_update["last_name"] = last_name

    return user.update(**to_update)
