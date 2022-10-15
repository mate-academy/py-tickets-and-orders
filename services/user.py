from db.models import User


def create_user(
    username: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    email: str = None
) -> None:
    user = User.objects.create_user(username)
    user.set_password(password)
    user.first_name = first_name if first_name else ""
    user.last_name = last_name if last_name else ""
    user.email = email if email else ""
    user.save()


def get_user(user_id) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id,
                username=None,
                password=None,
                first_name=None,
                last_name=None,
                email=None):
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
