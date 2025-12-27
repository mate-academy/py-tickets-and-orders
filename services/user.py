from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> User:

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                password: str = None,
                **user_data
                ) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)

    allowed_fields = ["first_name", "last_name", "email", "username"]
    for field in allowed_fields:
        if field in user_data:
            value = user_data[field]
            setattr(user, field, "" if value is None else value)

    for field in allowed_fields:
        current_value = getattr(user, field)
        if current_value is None:
            setattr(user, field, "")
    user.save()
