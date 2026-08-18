from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    extra_fields = {}
    if email:
        extra_fields["email"] = email
    if first_name:
        extra_fields["first_name"] = first_name
    if last_name:
        extra_fields["last_name"] = last_name
    return User.objects.create_user(
        username=username,
        password=password,
        **extra_fields
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = User.objects.get(pk=user_id)
    for key, value in kwargs.items():
        if key == "password":
            user.set_password(value)
        else:
            setattr(user, key, value)
    user.save()
