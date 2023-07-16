from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from django.db import transaction

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> User | None:
    new_user = None
    with transaction.atomic():
        new_user = get_user_model().objects.create_user(
            username=username,
            password=password
        )
        if email:
            new_user.email = email
        if last_name:
            new_user.last_name = last_name
        if first_name:
            new_user.first_name = first_name
        new_user.save()
    return new_user


def get_user(user_id: int) -> User | None:
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return None


def find_users(
    username: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> QuerySet[User]:
    search_creteria = Q()
    if username:
        search_creteria &= Q(username=username)
    if email:
        search_creteria &= Q(email=email)
    if first_name:
        search_creteria &= Q(first_name=first_name)
    if last_name:
        search_creteria &= Q(last_name=last_name)
    return User.objects.filter(search_creteria)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> User | None:
    user = get_user(user_id)
    if user:
        update = []
        if username:
            user.username = username
            update.append("username")
        if password:
            user.set_password(password)
            update.append("password")
        if email:
            user.email = email
            update.append("email")
        if first_name:
            user.first_name = first_name
            update.append("first_name")
        if last_name:
            user.last_name = last_name
            update.append("last_name")
        user.save(update_fields=update)
        return user
    return None
