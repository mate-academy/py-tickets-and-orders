from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    extra_fields = {}
    if email is not None:
        extra_fields["email"] = email
    if first_name is not None:
        extra_fields["first_name"] = first_name
    if last_name is not None:
        extra_fields["last_name"] = last_name

    real_user = User.objects.create_user(
        username=username,
        password=password,
        **extra_fields)
    return real_user


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
    got_it_user = get_user(user_id)

    if username is not None:
        got_it_user.username = username

    if password is not None:
        got_it_user.set_password(password)

    if email is not None:
        got_it_user.email = email

    if first_name is not None:
        got_it_user.first_name = first_name

    if last_name is not None:
        got_it_user.last_name = last_name

    got_it_user.save()

    return got_it_user
