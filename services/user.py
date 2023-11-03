from db.models import User


def create_user(
        username: str,
        password: str,
        email=None,
        first_name=None,
        last_name=None) -> User:
    user = User.objects.create_user(
        username,
        email=email,
        password=password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user


def get_user(user_id: int) -> User | None:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def update_user(
        user_id: int,
        username=None,
        password=None,
        email=None,
        first_name=None,
        last_name=None) -> User | None:
    try:
        user = User.objects.get(id=user_id)
        if username:
            user.username = username
        if password:
            user.set_password(password)
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        return user
    except User.DoesNotExist:
        return None
