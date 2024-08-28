from django.contrib.auth import get_user_model

from db.models import User


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> None:
    if get_user_model().objects.filter(username=username).exists():
        print(f'User "{username}" already exists')
        return

    user_data = {}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    get_user_model().objects.create_user(
        username=username,
        password=password,
        **user_data
    )


def get_user(user_id: int) -> User:
    return get_user_model().objects.filter(pk=user_id).first()


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    if not get_user_model().objects.filter(pk=user_id).exists():
        print(f'User with id = "{user_id}" does not exists')
        return

    user = get_user_model().objects.get(pk=user_id)

    if username:
        if (
            user.username != username
            and get_user_model().objects.filter(username=username).exists()
        ):
            print(f'User with username "{username}" already exists')
            return
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
