from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(username: str,
                password: str, email: str = None,
                first_name: str = None, last_name: str = None
                ) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or ""
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
    user_id : int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    password: str | None = None
) -> User:
    user = User.objects.get(id=user_id)
    user.first_name = first_name if first_name is not None else ""
    user.last_name = last_name if last_name is not None else ""
    user.email = email if email is not None else ""
    if username is not None:
        user.username = username
    if password:
        user.set_password(password)
    user.save()
    return user
