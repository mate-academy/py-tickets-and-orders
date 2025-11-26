# from django.db.models import QuerySet

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    query = User.objects.get(id=user_id)
    if username:
        query.username = username
    if password:
        query.set_password(password)
    if email:
        query.email = email
    if first_name:
        query.first_name = first_name
    if last_name:
        query.last_name = last_name

    query.save(update_fields=[
        "username",
        "password",
        "email",
        "first_name",
        "last_name"]
    )
