from typing import Optional
from db.models import User


def create_user(
    username: str,
    password: str,
    first_name: str = "",
    last_name: str = "",
    email: str = "",
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    return user


def get_user(user_id: int) -> Optional[User]:
    return User.objects.filter(id=user_id).first()


def update_user(user_id: int, **kwargs) -> Optional[User]:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None

    allowed_fields = {
        "username",
        "password",
        "first_name",
        "last_name",
        "email"
    }

    for field, value in kwargs.items():
        if field in allowed_fields:
            if field == "password":
                user.set_password(value)
            else:
                setattr(user, field, value)

    user.save()
    return user


def delete_user(user_id: int) -> None:
    User.objects.filter(id=user_id).delete()
