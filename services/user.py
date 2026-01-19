from db.models import User


def create_user(
    username: str,
    password: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    _user = User.objects.create_user(username, email, password)
    if first_name:
        _user.first_name = first_name
    if last_name:
        _user.last_name = last_name
    _user.save()
    return _user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: str = None,
    password: str = None,
    email: str = None,
    first_name: str = None,
    last_name: str = None
) -> None:
    update_us = User.objects.get(id=user_id)
    if username:
        update_us.username = username
    if password:
        update_us.set_password(password)
    if email:
        update_us.email = email
    if first_name:
        update_us.first_name = first_name
    if last_name:
        update_us.last_name = last_name
    update_us.save()
    return update_us
