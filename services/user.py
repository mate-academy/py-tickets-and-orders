from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    user_data = {"username": username, "password": password}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name
    return get_user_model().objects.create_user(**user_data)


def get_user(user_id: int) -> object:
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return f"User with id {user_id} does not exist."


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return f"User with id {user_id} does not exist."

    if username:
        user.username = username
    if password:
        try:
            password_validation.validate_password(password, user)
            user.set_password(password)
        except ValidationError:
            return "Password validation error."
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
