from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username: str, password: str, **kwargs) -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        **kwargs
    )


def get_user(user_id: int) -> User:
    return User.objects.filter(id=user_id).first()


def update_user(user_id: int, **kwargs) -> User:
    user = get_user(user_id)
    if user:
        if "password" in kwargs:
            user.set_password(kwargs.pop("password"))
        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
    return user
