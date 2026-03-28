from db.models import User


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> User:
    user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name)
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **info) -> User:
    user = User.objects.get(id=user_id)
    if "first_name" in info:
        user.first_name = info["first_name"]
    if "last_name" in info:
        user.last_name = info["last_name"]
    if "email" in info:
        user.email = info["email"]
    if "password" in info:
        user.set_password(info["password"])
    if "username" in info:
        user.username = info["username"]

    user.save()
    return user
