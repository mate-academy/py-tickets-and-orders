from django.core.exceptions import ValidationError

from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    if User.objects.filter(username=username).exists():
        raise ValidationError(f"Username {username} already exists")

    user_data = {"username": username, "password": password}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    return User.objects.create_user(**user_data)


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    user = get_user(user_id)
    if username:
        if (User.objects.filter(
                username=username).
                exclude(id=user_id).
                exists()):
            raise ValidationError(
                f"Username {username} already exists"
            )
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
