from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user_data = {
        "username": username,
        "password": password,
    }
    if email is not None:
        user_data["email"] = email
    if first_name is not None:
        user_data["first_name"] = first_name
    if last_name is not None:
        user_data["last_name"] = last_name

    user = User.objects.create_user(**user_data)
    return user


def get_user(user_id: int) -> User | None:
    return User.objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User | None:
    user = get_object_or_404(User, pk=user_id)
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
