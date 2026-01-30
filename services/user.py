from db.models import User


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user_info = User.objects.get(id=user_id)
    if username:
        user_info.username = username
    if password:
        user_info.set_password(password)
    if email:
        user_info.email = email
    if first_name:
        user_info.first_name = first_name
    if last_name:
        user_info.last_name = last_name
    user_info.save()
