from django.contrib.auth import get_user_model
from typing import Optional


User = get_user_model()


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None
                ) -> User:
    return User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name or "",
        last_name=last_name or ""
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None
) -> Optional[User]:
    try:
        user = get_user(user_id)
    except User.DoesNotExist:
        return None

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    elif first_name is None:
        user.first_name = ""
    if last_name is not None:
        user.last_name = last_name
    elif last_name is None:
        user.last_name = ""
    if password is not None:
        user.set_password(password)

    user.save()
    return user
