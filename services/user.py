from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                first_name: str = "",
                last_name: str = "",
                email: str = "") -> User:

    user_model = get_user_model()

    user = user_model(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    user.set_password(password)

    user.save()

    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user(user_id)

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
