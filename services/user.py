from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def create_user(username: str,
                password: str,
                first_name: str,
                last_name: str,
                email: str) -> User:

    """
    Creates a new user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.

    Returns:
        User: The created user.
    """
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists")

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    return user


def get_user(user_id: int) -> User:

    """
    Retrieves a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The user object.
    """
    return User.objects.get(id=user_id)


def update_user(user_id: int, username: str,
                password: str,
                email: str,
                first_name: str,
                last_name: str) -> User:
    """
    Updates a user's details.

    Args:
        user_id (int): The ID of the user.
        username (str): The new username of the user.
        password (str): The new password of the user.
        email (str): The new email of the user.
        first_name (str): The new first name of the user.
        last_name (str): The new last name of the user.

    Returns:
        User: The updated user object.
    """
    user = User.objects.get(id=user_id)

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
