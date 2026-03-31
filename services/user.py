from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> get_user_model():
    encrypted_password = make_password(password)
    user = get_user_model().objects.create(
        username=username,
        password=encrypted_password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> get_user_model() | None:
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return None


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> get_user_model():
    user = get_user(user_id)
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
    return user
