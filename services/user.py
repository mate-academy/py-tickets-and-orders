from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> User:
    """
    Create a new user with encrypted password.

    Args:
        username: Username for the new user
        password: Password (will be encrypted)
        email: Optional email address
        first_name: Optional first name
        last_name: Optional last name

    Returns:
        User: The created user instance
    """
    user = User.objects.create_user(username=username, password=password)

    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    # Save the user if any optional fields were set
    if email is not None or first_name is not None or last_name is not None:
        user.save()

    return user


def get_user(user_id: int) -> User:
    """
    Get a user by ID.

    Args:
        user_id: ID of the user to retrieve

    Returns:
        User: The user instance

    Raises:
        User.DoesNotExist: If user with given ID doesn't exist
    """
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> User:
    """
    Update a user's information.

    Args:
        user_id: ID of the user to update
        username: Optional new username
        password: Optional new password (will be encrypted)
        email: Optional new email address
        first_name: Optional new first name
        last_name: Optional new last name

    Returns:
        User: The updated user instance

    Raises:
        User.DoesNotExist: If user with given ID doesn't exist
    """
    user = User.objects.get(id=user_id)

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    # Handle password separately using set_password for proper encryption
    if password is not None:
        user.set_password(password)

    user.save()
    return user
