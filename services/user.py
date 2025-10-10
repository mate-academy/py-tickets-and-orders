from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email if email else "",
    )

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> Optional[User]:
    return User.objects.filter(id=user_id).first()


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
) -> bool:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return False

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
    return True
