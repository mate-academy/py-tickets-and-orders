from db.models import User
from typing import Optional


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    new_user = User.objects.create_user(
        username=username,
        password=password,
    )
    add_user_info(new_user, email, first_name, last_name)
    new_user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> None:
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    add_user_info(user, email, first_name, last_name)
    user.save()


def add_user_info(
        user: User,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
