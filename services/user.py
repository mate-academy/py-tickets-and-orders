from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user(user_id)

    if username is not None:
        user.username = username

    if email is not None:
        user.email = email

    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if password is not None:
        user.set_password(password)

    user.save()

    return user
