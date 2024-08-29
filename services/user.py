from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        email: str = None
) -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> User:

    geting_user = get_user(user_id)
    if username:
        geting_user.username = username
    if password:
        geting_user.set_password(password)
    if email:
        geting_user.email = email
    if first_name:
        geting_user.first_name = first_name
    if last_name:
        geting_user.last_name = last_name
    geting_user.save()
    return geting_user
