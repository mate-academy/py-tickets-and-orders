from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from db.models import User


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> User:
    from db.models import User
    user = User.objects.create_user(username=username, password=password)

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> User | None:
    from db.models import User
    try:
        user = User.objects.get(id=user_id)
        return user
    except ObjectDoesNotExist:
        return None


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> User | None:
    from db.models import User
    try:
        user = User.objects.get(id=user_id)

        if username:
            user.username = username
        if password:
            user.set_password(password)  # Ensure the password is encrypted
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()
        return user
    except ObjectDoesNotExist:
        return None
