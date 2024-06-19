from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = User.objects.create_user(username=username,
                                    password=password)
    changes_exists = False
    if email:
        user.email = email
        changes_exists = True
    if first_name:
        user.first_name = first_name
        changes_exists = True
    if last_name:
        user.last_name = last_name
        changes_exists = True
    if changes_exists:
        user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(pk=user_id)


def update_user(user_id: int,
                password: str = None,
                username: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> None:
    user = User.objects.get(pk=user_id)
    changes_exists = False
    if email:
        user.email = email
        changes_exists = True
    if first_name:
        user.first_name = first_name
        changes_exists = True
    if last_name:
        user.last_name = last_name
        changes_exists = True
    if username:
        user.username = username
        changes_exists = True
    if password:
        user.set_password(password)
        changes_exists = True
    if changes_exists:
        user.save()
