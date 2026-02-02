from db.models import User


def create_user(
    username: str,
    password: str,
    **kwargs
) -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
    user_id: int,
    password: str = None,
    **kwargs
) -> None:
    user = User.objects.get(pk=user_id)

    if password:
        user.set_password(password)

    if kwargs:
        for name, value in kwargs.items():
            user.__dict__[name] = value
    user.save()
