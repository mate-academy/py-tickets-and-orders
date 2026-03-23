from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def get_user(user_id: int = None, username: str = None) -> User:
    """Return user by ID or username."""
    if user_id:
        return User.objects.get(id=user_id)
    if username:
        return User.objects.get(username=username)
    raise ValueError("user_id or username must be provided")


@transaction.atomic
def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> User:
    user = User.objects.create_user(username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


@transaction.atomic
def update_user(
    user_id: int = None,
    username: str = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> User:
    user = get_user(user_id=user_id, username=username)

    if password:
        user.set_password(password)
    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user
