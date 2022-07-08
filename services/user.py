from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email=None,
        first_name=None,
        last_name=None
):
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
    )

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    user.save()


def get_user(user_id):
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id: int,
        username=None,
        password=None,
        email=None,
        first_name=None,
        last_name=None
):
    new_user = get_user(user_id)

    if username is not None:
        new_user.username = username

    if password is not None:
        new_user.set_password(password)

    if email is not None:
        new_user.email = email

    if first_name is not None:
        new_user.first_name = first_name

    if last_name is not None:
        new_user.last_name = last_name

    new_user.save()
