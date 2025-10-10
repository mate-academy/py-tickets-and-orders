from django.contrib.auth import get_user_model
from typing import Optional

User = get_user_model()


def create_user(username: str, email: str, password: str) -> str:

    return User.objects.create_user(username=username,
                                    email=email, password=password)


def get_user_by_username(username: str) -> Optional[User]:

    return User.objects.filter(username=username).first()


def update_user_email(username: str, new_email: str) -> bool:

    user = User.objects.filter(username=username).first()
    if not user:
        return False

    user.email = new_email
    user.save()
    return True
