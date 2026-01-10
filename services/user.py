from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> User | None:
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return None


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User | None:
    user = get_user(user_id)
    if not user:
        return None

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
