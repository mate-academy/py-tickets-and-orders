from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None
):
    new_user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name
    if email:
        new_user.email = email
    new_user.save()

    return new_user


def get_user(user_id):
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None
):
    user = get_user(user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    user.save()
