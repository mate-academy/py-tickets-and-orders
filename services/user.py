from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
    )

    fields = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }

    for field, value in fields.items():
        if value is not None:
            setattr(user, field, value)

    user.save()
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    user = get_user(user_id)

    if username is not None:
        user.username = username

    if password is not None:
        user.set_password(password)

    fields = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }

    for field, value in fields.items():
        if value is not None:
            setattr(user, field, value)

    user.save()
    return user
