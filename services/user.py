from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_user(username: str,
                password: str,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None) -> QuerySet[get_user_model()]:
    user = get_user_model()
    user = user.objects.create_user(username=username, password=password)

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> QuerySet[get_user_model()]:
    user = get_user_model()
    user = user.objects.get(pk=user_id)
    return user


def update_user(user_id: int,
                username: str | None = None,
                password: str | None = None,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None) -> QuerySet[get_user_model()]:
    user = get_user_model()
    user = user.objects.get(pk=user_id)
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
