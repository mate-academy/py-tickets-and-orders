from typing import Optional

from django.contrib.auth import get_user_model

User = get_user_model()


def update_user_fields(user: object,
                       username: Optional[str] = None,
                       password: Optional[str] = None,
                       email: Optional[str] = None,
                       first_name: Optional[str] = None,
                       last_name: Optional[str] = None
                       ) -> None:
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


def create_user(username: str,
                password: str,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    new_user = get_user_model().objects.create_user(
        username=username, password=password
    )
    update_user_fields(
        new_user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> None:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> None:
    updated_user = get_user_model().objects.get(id=user_id)
    update_user_fields(updated_user,
                       username=username,
                       password=password,
                       email=email,
                       first_name=first_name,
                       last_name=last_name
                       )
