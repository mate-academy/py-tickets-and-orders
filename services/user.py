from db.models import User


def create_user_data(
        user: User,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
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
    user = User.objects.create_user(username=username, password=password)

    create_user_data(user, email, first_name, last_name)


def get_user(user_id: int) -> User:
    user = User.objects.get(id=user_id)
    return user


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    create_user_data(user, email, first_name, last_name)
