from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    fields = {
        field: value for field, value in [
            ("username", username),
            ("password", password),
            ("email", email),
            ("first_name", first_name),
            ("last_name", last_name)
        ] if value is not None
    }

    get_user_model().objects.create_user(**fields)


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user(user_id)

    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
