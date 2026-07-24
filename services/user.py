from db.models import User


def create_user(username: str, password: str, email: str = None,
                first_name: str = None, last_name: str = None) -> User:
    extra_fields = {}

    if email is not None:
        extra_fields["email"] = email
    if first_name is not None:
        extra_fields["first_name"] = first_name
    if last_name is not None:
        extra_fields["last_name"] = last_name

    user = User.objects.create_user(
        username=username, password=password, **extra_fields
    )

    return user


def get_user(user_id: int) -> User:
    user = User.objects.get(pk=user_id)
    return user


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
) -> User:
    user = User.objects.get(id=user_id)

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
