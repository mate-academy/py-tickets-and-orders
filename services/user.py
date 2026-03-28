from django.contrib.auth import get_user_model
from typing import Optional

# Get the correct User model (handles custom user models automatically)
User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> User:
    """
    Create a new user with an encrypted password and optional details.

    :param username: The username for the new user.
    :param password: The password (will be encrypted).
    :param email: (Optional) Email of the user.
    :param first_name: (Optional) First name of the user.
    :param last_name: (Optional) Last name of the user.
    :return: The created User object.
    """
    user = User.objects.create_user(username=username, password=password)

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> Optional[User]:
    """
    Retrieve a user by ID.

    :param user_id: The ID of the user to retrieve.
    :return: The User object if found, else None.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Optional[User]:
    """
    Update an existing user with new values if provided.

    :param user_id: The ID of the user to update.
    :param username: (Optional) New username.
    :param password: (Optional) New password (will be encrypted).
    :param email: (Optional) New email.
    :param first_name: (Optional) New first name.
    :param last_name: (Optional) New last name.
    :return: The updated User object if found, else None.
    """
    try:
        user = User.objects.get(id=user_id)

        if username:
            user.username = username
        if password:
            user.set_password(password)  # Ensures password encryption
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()
        return user
    except User.DoesNotExist:
        return None
