from django.contrib.auth import get_user_model

CustomUser = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> CustomUser:
    return CustomUser.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> CustomUser:
    return CustomUser.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> CustomUser:
    user_to_update = get_user(user_id)

    if username:
        user_to_update.username = username
    if email:
        user_to_update.email = email
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name
    if password:
        user_to_update.set_password(password)
    user_to_update.save()
