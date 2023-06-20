from db.models import User


def create_user(
        username: str,
        password: str,
        **kwargs
) -> None:
    new_user = User.objects.create_user(
        username=username,
        password=password
    )
    for attribute, value in kwargs.items():
        setattr(new_user, attribute, value)

    new_user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        password: str = None,
        **kwargs
) -> None:
    user = get_user(user_id=user_id)

    if password:
        user.set_password(password)

    for attribute, value in kwargs.items():
        setattr(user, attribute, value)

    user.save()
