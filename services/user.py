from db.models import User


def create_user(**kwargs) -> User:
    return User.objects.create_user(**kwargs)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = User.objects.get(id=user_id)
    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))
    for field, value in kwargs.items():
        setattr(user, field, value)
    user.save()
    return user
