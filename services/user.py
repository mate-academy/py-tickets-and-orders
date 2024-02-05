from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
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
    return User.objects.get(
        id=user_id
    )


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:

    user_for_update = get_user(user_id)

    if username:
        user_for_update.username = username
    if password:
        user_for_update.set_password(password)
    if email:
        user_for_update.email = email
    if first_name:
        user_for_update.first_name = first_name
    if last_name:
        user_for_update.last_name = last_name

    user_for_update.save()
