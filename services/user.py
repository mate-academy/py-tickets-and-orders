from django.contrib.auth import get_user_model
from django.db.models import QuerySet


User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> QuerySet:
    extra_fields = {}
    if email:
        extra_fields["email"] = email
    if first_name:
        extra_fields["first_name"] = first_name
    if last_name:
        extra_fields["last_name"] = last_name

    user = User.objects.create_user(
        username=username,
        password=password,
        **extra_fields
    )
    return user


def get_user(user_id: int) -> QuerySet:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> QuerySet:
    user = get_user(user_id)

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user
