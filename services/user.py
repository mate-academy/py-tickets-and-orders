from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str,
        password: str,
        **kwargs
) -> User:
    return User.objects.create_user(
        username=username,
        password=password, **kwargs
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = get_user(user_id)
    password = kwargs.pop("password", None)
    if password:
        user.set_password(password)
    for field, value in kwargs.items():
        setattr(user, field, value)

    user.save()
    return user
