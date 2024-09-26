from typing import Optional
from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    User.objects.create_user(
        username=username,
        password=password,
        email=email if email else "",
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else ""
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    current_user = User.objects.get(pk=user_id)
    if username:
        current_user.username = username
    if password:
        current_user.set_password(password)
    if email:
        current_user.email = email
    if first_name:
        current_user.first_name = first_name
    if last_name:
        current_user.last_name = last_name
    current_user.save()
