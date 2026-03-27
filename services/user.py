from django.contrib.auth import get_user_model

from db.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> User:
    user, created = User.objects.get_or_create(email=email, defaults={
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    })
    if not created:
        raise ValidationError(f"User with email '{email}' already exists.")
    user.set_password(password)
    user.save()
    return user


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with id '{user_id}' does not exist.")


def update_user(user_id: int, username: str = "",
                password: str = "",
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> User:
    user = get_user(user_id)

    if email and get_user_model().objects.filter(
            email=email
    ).exclude(id=user_id).exists():
        raise ValidationError(
            f"Email '{email}' is already used by another user."
        )

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user
