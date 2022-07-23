from django.contrib.auth import get_user_model


def create_user(
        username, password,
        email=None, first_name=None,
        last_name=None):
    created_user = get_user_model().objects.create_user(username=username,
                                                        password=password)

    if email:
        created_user.email = email
    if first_name:
        created_user.first_name = first_name
    if last_name:
        created_user.last_name = last_name

    created_user.save()

    return created_user


def get_user(user_id):
    return get_user_model().objects.get(id=user_id)


def update_user(
        user_id,
        username=None,
        password=None,
        email=None,
        first_name=None,
        last_name=None
):
    updated_user = get_user_model().objects.get(id=user_id)

    if username:
        updated_user.username = username
    if password:
        updated_user.set_password(password)
    if email:
        updated_user.email = email
    if first_name:
        updated_user.first_name = first_name
    if last_name:
        updated_user.last_name = last_name

    updated_user.save()
