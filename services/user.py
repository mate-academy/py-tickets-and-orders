from django.contrib.auth import get_user_model
from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> None:
    user = get_user_model().objects.create_user(
        username=username, password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if first_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    if user_id:
        return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> User:
    cur_user = get_user(user_id)
    if username:
        cur_user.username = username
    if password:
        cur_user.set_password(password)
    if email:
        cur_user.email = email
    if first_name:
        cur_user.first_name = first_name
    if last_name:
        cur_user.last_name = last_name
    cur_user.save()
    return cur_user
