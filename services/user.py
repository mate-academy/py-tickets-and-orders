from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str, password: (str, int), email: str = None,
                first_name: str = None, last_name: str = None) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    """Getting user with the given id"""
    return User.objects.get(id=user_id)


def update_user(user_id: int, username: str = None,
                password: (str, int) = None, email: str = None,
                first_name: str = None, last_name: str = None) -> None:
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
