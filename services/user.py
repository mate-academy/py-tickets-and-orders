from django.contrib.auth import get_user_model


def create_user(username: str,
                password: (str | int),
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> get_user_model:
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
    return user.save()


def get_user(user_id: int) -> get_user_model:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: (str | int) = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> get_user_model:
    user_ = get_user(user_id)
    if password is not None:
        user_.set_password(password)

    if username is not None:
        user_.username = username

    if email is not None:
        user_.email = email

    if first_name is not None:
        user_.first_name = first_name

    if last_name is not None:
        user_.last_name = last_name

    return user_.save()
