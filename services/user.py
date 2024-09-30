from django.contrib.auth import get_user_model


def create_user(
    username: str,
    password: str,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    user = get_user_model().objects.create_user(
        username=username,
        password=password
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(pk=user_id)


def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> None:
    updates = {}

    if username:
        updates["username"] = username
    if email:
        updates["email"] = email
    if first_name:
        updates["first_name"] = first_name
    if last_name:
        updates["last_name"] = last_name

    if password:
        user = get_user(user_id)
        user.set_password(password)
        user.save()

    if updates:
        get_user_model().objects.filter(pk=user_id).update(**updates)
