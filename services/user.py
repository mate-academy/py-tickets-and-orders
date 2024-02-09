from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = "",
        last_name: str = ""
) -> User:
    with transaction.atomic():
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
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
) -> User:
    user = get_user(user_id)
    with transaction.atomic():
        if username:
            try:
                UnicodeUsernameValidator(username)
                user.username = username
            except ValidationError as e:
                raise e
            user.username = username
        if password:
            try:
                validate_password(password)
                user.set_password(raw_password=password)
            except ValidationError as e:
                raise e
        if email:
            try:
                validate_email(email)
                user.email = email
            except ValidationError as e:
                raise e
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()

        return user
