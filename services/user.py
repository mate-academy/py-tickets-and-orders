from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    return user


def update_user(
        user_id: int,
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = get_user(user_id)

    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)

    user.save()
    return user
