from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    user_data = {}
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    return User.objects.create_user(
        username=username,
        password=password,
        **user_data
    )


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None
                ) -> None:
    user_data = {}
    user = User.objects.get(pk=user_id)
    if password:
        user.set_password(password)
        user.save()
    if username:
        user_data["username"] = username
    if email:
        user_data["email"] = email
    if first_name:
        user_data["first_name"] = first_name
    if last_name:
        user_data["last_name"] = last_name

    User.objects.filter(
        pk=user_id
    ).update(**user_data)
