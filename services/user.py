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
    user = User.objects.get(user__id=user_id)
    return user


def update_user():
    pass
