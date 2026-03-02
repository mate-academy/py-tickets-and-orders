from typing import Optional

from db.models import User


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
    )

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> Optional[User]:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def update_user(user_id: int, password: str = None, **kwargs) -> None | User:
    user = get_user(user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    if password:
        user.set_password(password)
    user.save()
    return user
