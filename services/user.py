from db.models import User
from django.contrib.auth.hashers import make_password


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = "",

):
    return User.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int):
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        password: str = None,
        **kwargs
) -> User:

    user = User.objects.get(id=user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)

    if password:
        user.set_password(password)

    user.save()
    return user
