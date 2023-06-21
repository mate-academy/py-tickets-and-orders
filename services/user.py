from django.db.models import QuerySet
from db.models import User
from django.contrib.auth import get_user_model
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        *args,
        **kwargs
) -> User:
    new_user = User(username=username, *args, **kwargs)

    if email is not None:
        setattr(new_user, "email", email)

    if first_name is not None:
        setattr(new_user, "first_name", first_name)

    if last_name is not None:
        setattr(new_user, "last_name", last_name)

    new_user.set_password(password)

    new_user.save()

    return new_user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> QuerySet:
    user = get_user_model().objects.filter(id=user_id)

    if password is not None:
        user_update = get_user(user_id)
        user_update.set_password(password)
        user_update.save()

    user_to_update = {}

    if username is not None:
        user_to_update["username"] = username

    if email is not None:
        user_to_update["email"] = email

    if first_name is not None:
        user_to_update["first_name"] = first_name

    if last_name is not None:
        user_to_update["last_name"] = last_name

    return user.update(**user_to_update)
