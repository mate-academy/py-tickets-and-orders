from typing import Optional

from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def create_user(
        username: str,
        password: str,
        email: Optional[str] = "",
        first_name: Optional[str] = "",
        last_name: Optional[str] = ""
) -> CustomUser:
    return CustomUser.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> CustomUser:
    return CustomUser.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> CustomUser:
    user_to_update = get_user(user_id)

    if username:
        user_to_update.username = username
    if email:
        user_to_update.email = email
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name
    if password:
        user_to_update.set_password(password)
    user_to_update.save()
