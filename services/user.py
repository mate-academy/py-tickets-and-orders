from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

User = get_user_model()


def email_validator(email: str) -> None:
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Wrong email structure")


def name_validator(name: str) -> None:
    if not name.isalpha():
        raise ValueError(f"Name {name} shoud be alpabet")


def create_user(username: str,
                password: str,
                email: models.EmailField = None,
                first_name: str = None,
                last_name: str = None) -> None:
    if email:
        email_validator(email)

    User.objects.create_user(username=username,
                             email=(email or ""),
                             first_name=(first_name or ""),
                             last_name=(last_name or ""),
                             password=password)


def get_user(user_id: int) -> User | None:
    try:
        man = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None
    return man


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: models.EmailField = None,
                first_name: str = None,
                last_name: str = None) -> None | str:

    user = get_user(user_id)
    if not user:
        return (f"No such user with id ={user_id}")
    if email:
        email_validator(email)
        user.email = email
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if first_name:
        name_validator(first_name)
        user.first_name = first_name
    if last_name:
        name_validator(last_name)
        user.last_name = last_name
    user.save()
