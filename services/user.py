from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str, password: str,
        email: str = None, first_name: str = None,
        last_name: str = None
) -> None:
    user = User.objects.create_user(
        username=username,
        password=password
    )
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None, password: str = None,
        first_name : str = None, last_name: str = None,
        email: str = None
) -> None:
    user = get_user(user_id)
    count = 0
    if username is not None:
        count += 1
        user.username = username
    if password is not None:
        count += 1
        user.set_password(password)
    if first_name is not None:
        count += 1
        user.first_name = first_name
    if last_name is not None:
        count += 1
        user.last_name = last_name
    if email is not None:
        count += 1
        user.email = email

    if count > 0:
        user.save()
