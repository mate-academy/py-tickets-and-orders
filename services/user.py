from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import User


def create_user(username: str, password: str, first_name: str, last_name: str, email: str) -> User:

    user = User.objects.create_user(username=username, password=password)

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email

    user.save()
    return user


def get_user(user_id: int) -> int:
    return User.objects.get(id=user_id)


def update_user(user_id: int, username: str, password: str, first_name: str, last_name: str, email: str) -> None:
    User.objects.update_or_create(id=user_id, defaults={"username": username, "first_name": first_name,
                                                        "last_name": last_name, "email": email})
    if password:
        User.set_password(password)

    User.save()
