from django.shortcuts import get_object_or_404

from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:

    user_data = {
        "username": username,
        "password": password
    }
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    some_user = User.objects.create_user(**user_data)
    return some_user


def get_user(user_id: int) -> User:
    return get_object_or_404(User, id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    updated_user = User.objects.get(id=user_id)

    if username:
        updated_user.username = username
    if email:
        updated_user.email = email
    if first_name:
        updated_user.first_name = first_name
    if last_name:
        updated_user.last_name = last_name
    if password:
        updated_user.set_password(password)

    updated_user.save()

    return updated_user
