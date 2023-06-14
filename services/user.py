from db.models import User


def create_user(*args, **kwargs) -> User:
    user = User.objects.create_user(
        *args, **kwargs
    )
    user.save()
    return user


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = User.objects.get(id=user_id)

    for key, value in kwargs.items():
        if value is not None:
            if key == "password":
                user.set_password(value)
            else:
                setattr(user, key, value)

    user.save()
    return user
