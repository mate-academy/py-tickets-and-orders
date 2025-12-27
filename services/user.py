from django.contrib.auth import get_user_model

User = get_user_model()


def filter_none(**kwargs) -> dict:
    return {key: value for key, value in kwargs.items() if value is not None}


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    valid_data = filter_none(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    user = User.objects.create_user(**valid_data)

    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    valid_data = filter_none(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    user = get_user(user_id)

    if "password" in valid_data:
        user.set_password(valid_data["password"])
        del valid_data["password"]

    for field, value in valid_data.items():
        setattr(user, field, value)

    user.save()
