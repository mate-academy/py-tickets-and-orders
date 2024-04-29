from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email if email else "",
        first_name=first_name if first_name else "",
        last_name=last_name if last_name else ""
    )


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user(user_id)
    user.username = username if username else user.username
    user.email = email if email else user.email
    user.first_name = first_name if first_name else user.first_name
    user.last_name = last_name if last_name else user.last_name
    if password:
        user.set_password(password)
    user.save()
