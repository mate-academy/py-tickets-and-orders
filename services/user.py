from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = User.objects.get(pk=user_id)

    updated_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }

    fields_to_update = []

    for key, value in updated_data.items():
        if value is not None:
            setattr(user, key, value)
            fields_to_update.append(key)

    if password is not None:
        user.set_password(password)
        fields_to_update.append("password")

    if fields_to_update:
        user.save(update_fields=fields_to_update)

    return user
