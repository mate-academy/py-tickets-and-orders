from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    data = ["email", "first_name", "last_name"]
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    for key, value in kwargs.items():
        if key in data:
            setattr(user, key, value)
        user.save()


def get_user(user_id: int) -> QuerySet:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user_updates = get_user(user_id)
    if username:
        user_updates.username = username
    if password:
        user_updates.set_password(password)
    if email:
        user_updates.email = email
    if first_name:
        user_updates.first_name = first_name
    if last_name:
        user_updates.last_name = last_name

    user_updates.save()
