from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: str = "",
    first_name: str = "",
    last_name: str = "",
) -> User:
    new_user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return new_user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = User.objects.get(id=user_id)

    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))

    for attr, value in kwargs.items():
        setattr(user, attr, value)

    user.save()
    return user
