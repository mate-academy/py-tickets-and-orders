from django.contrib.auth import get_user_model
from db.models import User


def user_setter(
    user: User,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    """Set user attributes based on provided values."""
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


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    """Create a new user."""
    new_user = get_user_model().objects.create_user(username=username)

    user_setter(
        new_user,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> None:
    """Update an existing user."""
    user_to_modify = get_user(user_id)

    user_setter(
        user_to_modify,
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def get_user(user_id: int) -> User:
    """Get a user by ID."""
    return User.objects.get(id=user_id)
