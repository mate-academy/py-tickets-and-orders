from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str, password: str, first_name: str = None,
                last_name: str = None, email: str = None) -> User:

    user = User.objects.create_user(username=username, password=password)

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email

    user.save()
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, username: str = None,
                password: str = None, first_name: str = None,
                last_name: str = None, email: str = None) -> None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError(f"User with id {user_id} does not exist")

    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if password:
        user.set_password(password)
    user.save()
