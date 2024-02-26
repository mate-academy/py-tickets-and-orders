from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password
    )

    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name

    new_user.save()


def get_user(user_id: int) -> get_user_model:
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    selected_user = get_user(user_id)

    if username:
        selected_user.username = username
    if password:
        selected_user.set_password(password)
    if email:
        selected_user.email = email
    if first_name:
        selected_user.first_name = first_name
    if last_name:
        selected_user.last_name = last_name

    selected_user.save()
