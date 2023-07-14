from typing import Optional

from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user_data = {
        "username": username,
        "password": password
    }
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name
    user = User.objects.create_user(**user_data)
    user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = get_user(user_id)
    user_new_data = {}
    if username:
        user_new_data["username"] = username
    if password:
        user.set_password(password)
    if email:
        user_new_data["email"] = email
    if first_name:
        user_new_data["first_name"] = first_name
    if last_name:
        user_new_data["last_name"] = last_name
    user.__dict__.update(user_new_data)
    user.save()
