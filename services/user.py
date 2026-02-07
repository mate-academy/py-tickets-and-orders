from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = "",
                last_name: str = "") -> User:
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


def get_user(user_id: int) -> None:
    return User.objects.get(id=user_id)


def update_user(user_id: int = None,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist():
        return None

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if password is not None:
        user.set_password(password)

    user.save()
    return user
