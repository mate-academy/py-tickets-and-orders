from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def create_user(username: str, password: str,
                first_name: str = "", last_name: str = "",
                email: str = "") -> QuerySet:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    return user


def get_user(user_id: int) -> int:
    return User.objects.get(id=user_id)


def update_user(user_id: int, username: str = None,
                password: str = None, email: str = None,
                first_name: str = None, last_name: str = None) -> QuerySet:
    user = User.objects.get(id=user_id)
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
