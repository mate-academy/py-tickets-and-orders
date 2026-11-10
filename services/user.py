from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user_data = {
        "username": username,
        "password": password,
    }
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name
    return User.objects.create_user(**user_data)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user_for_update = User.objects.get(id=user_id)

    if username:
        user_for_update.username = username

    if password:
        user_for_update.set_password(password)

    if email:
        user_for_update.email = email

    if first_name:
        user_for_update.first_name = first_name

    if last_name:
        user_for_update.last_name = last_name

    user_for_update.save()
