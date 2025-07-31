from typing import Optional

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> Optional[User]:
    user_obj = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name or "",
        last_name=last_name or "",
    )
    return user_obj


def get_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
) -> User:
    lookup_kwargs = {}
    if user_id:
        lookup_kwargs["pk"] = user_id
    if username:
        lookup_kwargs["username"] = username
    if password:
        lookup_kwargs["password"] = password
    if email:
        lookup_kwargs["email"] = email
    if first_name:
        lookup_kwargs["first_name"] = first_name

    user_obj = User.objects.get(**lookup_kwargs)
    return user_obj


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user_obj = User.objects.get(pk=user_id)
    if username:
        user_obj.username = username
    if password:
        user_obj.set_password(password)
    if email:
        user_obj.email = email
    if first_name:
        user_obj.first_name = first_name
    if last_name:
        user_obj.last_name = last_name
    user_obj.save()
