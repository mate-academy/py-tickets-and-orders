from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user_to_create = User(username=username)
    user_to_create.set_password(password)
    if email:
        user_to_create.email = email
    if first_name:
        user_to_create.first_name = first_name
    if last_name:
        user_to_create.last_name = last_name

    user_to_create.save()


def get_user(
        user_id: int
) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user_to_update = get_user(user_id=user_id)

    if username:
        user_to_update.username = username

    if password:
        user_to_update.set_password(password)

    if email:
        user_to_update.email = email

    if first_name:
        user_to_update.first_name = first_name

    if last_name:
        user_to_update.last_name = last_name

    user_to_update.save()
