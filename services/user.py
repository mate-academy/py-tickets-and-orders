from django.core.exceptions import ObjectDoesNotExist

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = User.objects.create_user(
        username=username,
        password=password,
    )
    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User not found")


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    try:
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
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("User not found")
