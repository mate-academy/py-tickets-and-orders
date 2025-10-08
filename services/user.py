from django.contrib.auth import get_user_model


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> get_user_model():

    optional_fields = {}
    if email:
        optional_fields["email"] = email
    if first_name:
        optional_fields["first_name"] = first_name
    if last_name:
        optional_fields["last_name"] = last_name

    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        **optional_fields
    )
    return user


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    user = get_user_model().objects.get(pk=user_id)

    if password:
        user.set_password(password)
    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
