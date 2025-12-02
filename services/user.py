from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None,
                ) -> None:
    user = get_user_model()
    user_object = user.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if first_name:
        user_object.first_name = first_name

    if last_name:
        user_object.last_name = last_name
    user_object.save()


def get_user(user_id: int) -> type[AbstractUser]:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user_object = get_user(user_id)
    if username:
        user_object.username = username
    if email:
        user_object.email = email
    if first_name:
        user_object.first_name = first_name
    if last_name:
        user_object.last_name = last_name
    if password:
        user_object.set_password(password)

    user_object.save()
