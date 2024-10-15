from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    update_user(
        user_id=user.id,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)
    user_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    for attr, value in user_data.items():
        if value is not None:
            setattr(user, attr, value)

    user.save()
