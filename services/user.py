from django.contrib.auth import get_user_model

from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
) -> User:
    new_user = get_user_model().objects.create_user(
        username=username,
    )
    new_user.set_password(password)
    new_user.save()
    update_user(
        user_id=new_user.id,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return new_user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
) -> User:
    user_to_update = User.objects.get(id=user_id)
    if username:
        user_to_update.username = username
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name
    if email:
        user_to_update.email = email
    if password:
        user_to_update.set_password(password)
    user_to_update.save()

    return user_to_update
