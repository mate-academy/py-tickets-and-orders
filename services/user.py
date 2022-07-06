from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email=None,
        first_name=None,
        last_name=None
):
    if not email:
        email = ""

    if not first_name:
        first_name = ""

    if not last_name:
        last_name = ""

    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


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
    new_user = get_user_model().objects.get(id=user_id)

    if username is not None:
        new_user.username = username

    if password is not None:
        new_user.set_password(password)

    if email is not None:
        new_user.email = email

    if first_name is not None:
        new_user.first_name = first_name

    if last_name is not None:
        last_name.username = last_name

    new_user.save()
