from django.contrib.auth import get_user_model
User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:

    if User.objects.filter(username=username).exists():
        raise ValueError(
            f"User with username '{username}' already exists")

    if email and User.objects.filter(email=email).exists():
        raise ValueError(
            f"User with email '{email}' already exists")

    extra_fields = {}
    if email:
        extra_fields["email"] = email
    if first_name:
        extra_fields["first_name"] = first_name
    if last_name:
        extra_fields["last_name"] = last_name

    user = User.objects.create_user(
        username=username,
        password=password,
        **extra_fields
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = get_user(user_id)
    fields = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    }
    for field, value in fields.items():
        if value is not None:
            setattr(user, field, value)
    if password:
        user.set_password(password)

    user.save()
