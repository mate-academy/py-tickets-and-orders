from db.models import User


def save_user_data(user: User, arguments: dict) -> None:
    for key, value in arguments.items():
        if key == "email":
            user.email = value
        if key == "first_name":
            user.first_name = value
        if key == "last_name":
            user.last_name = value
        if key == "username":
            user.username = value
        if key == "password":
            user.set_password(value)

        user.save()


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    user = User.objects.create_user(
        username=username,
        password=password,
    )

    save_user_data(user, kwargs)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        **kwargs
) -> None:
    user = User.objects.get(id=user_id)

    save_user_data(user, kwargs)
