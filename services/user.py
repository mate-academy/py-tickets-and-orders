from db.models import User


def save_user_data(user: User, arguments: dict) -> None:
    for field, value in arguments.items():
        if field in ["email", "first_name", "last_name", "username"]:
            setattr(user, field, value)
        elif field == "password":
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
