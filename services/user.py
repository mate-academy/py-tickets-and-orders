from django.contrib.auth import get_user_model


def create_user(username: str,
                password: str,
                email: str = None,
                first_name:
                str = None,
                last_name: str = None) -> "db.models.User":
    email_value = email
    if first_name is not None:
        first_name_value = first_name
    else:
        first_name_value = ""
    if last_name is not None:
        last_name_value = last_name
    else:
        last_name_value = ""
    usermodel = get_user_model()
    return usermodel.objects.create_user(
        username=username,
        password=password,
        email=email_value,
        first_name=first_name_value,
        last_name=last_name_value,
    )


def get_user(user_id: int) -> "db.models.User":
    return get_user_model().objects.get(pk=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = get_user(user_id)
    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    user.save()
