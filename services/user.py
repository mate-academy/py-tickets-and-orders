from typing import Optional

from db.models import User


def create_or_update_email_and_name(
        user: User,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    new_user = User.objects.create_user(username=username, password=password)

    create_or_update_email_and_name(
        user=new_user,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    new_user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user_to_update = get_user(user_id)

    if username:
        user_to_update.username = username

    if password:
        user_to_update.set_password(password)

    create_or_update_email_and_name(
        user=user_to_update,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user_to_update.save()
