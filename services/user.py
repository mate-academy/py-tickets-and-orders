from django.contrib.auth import get_user_model
from db.models import User

User_Model = get_user_model()


def create_user(
    username: str,
    password: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> User:
    user = User_Model.objects.create_user(username=username)
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    user.save()
    return user


def get_user(user_id: int) -> User:
    return User_Model.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> User:
    user = User_Model.objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    user.save()
    return user
