from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)
    user.save()
    return user


def get_user(user_id: int) -> User:
    user = User.objects.get(id=user_id)
    return user


def update_user(
        user_id: int,
        username: str = "",
        password: str = "",
        email: str = "",
        first_name: str = "",
        last_name: str = ""
) -> User:

    user = User.objects.get(id=user_id)
    if username:
        user.username = username

    if email:
        user.email = email

    if first_name:
        user.first_name = first_name

    if last_name:
        user.last_name = last_name

    if password:
        user.password = user.set_password(password)

    user.save()
    return user
