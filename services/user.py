from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    new_user = User.objects.create_user(
        username=username,
        password=password,
    )
    if email:
        new_user.email = email

    if first_name:
        new_user.first_name = first_name

    if last_name:
        new_user.last_name = last_name

    new_user.save()
    return new_user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:
    current_user = User.objects.get(pk=user_id)

    if username:
        current_user.username = username

    if password:
        current_user.set_password(password)

    if email:
        current_user.email = email

    if first_name:
        current_user.first_name = first_name

    if last_name:
        current_user.last_name = last_name

    current_user.save()
    return current_user
