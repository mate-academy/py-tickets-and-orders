from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def create_user(
    username: str,
    password: str,
    email: str,
    first_name: str,
    last_name: str) -> User:
    User = get_user_model()
    user = User.objects.create(username="username")
    if email:
        user.email = email
    if first_name:
        user.first_name  = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: str) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: str,
    username: str,
    password: str,
    email: str,
    first_name: str,
    last_name: str) -> User:
    user = User.objects.get(id=user_id)
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
