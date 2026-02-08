from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = User.objects.create_user(username=username, password=password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


User = get_user_model()


def get_user(user_id: int) -> list:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> User:
    user = get_user(user_id)

    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))

    for field, value in kwargs.items():
        setattr(user, field, value)

    user.save()
    return user
