from typing import Optional

from db.models import User


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None,
                ) -> User:
    user_obj = User(username=username)
    user_obj.set_password(password)
    if email:
        user_obj.email = email
    if first_name:
        user_obj.first_name = first_name
    if last_name:
        user_obj.last_name = last_name
    return user_obj.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None
                ) -> None:
    user_obj = User.objects.get(id=user_id)

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
