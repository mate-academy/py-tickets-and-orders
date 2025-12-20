from db.models import User


def create_user(username: str, password: str, email: str = "") -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = User.objects.get(id=user_id)
    for field, value in kwargs.items():
        setattr(user, field, value)
    user.save()
    return user
