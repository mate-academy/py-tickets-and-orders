from db.models import User


def create_user(
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        email: str = None,
) -> User:
    User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )


def get_user(
        user_id: int
) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    if username:
        User.objects.filter(id=user_id).update(username=username)
    if password:
        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()
    if email:
        User.objects.filter(id=user_id).update(email=email)
    if first_name:
        User.objects.filter(id=user_id).update(first_name=first_name)
    if last_name:
        User.objects.filter(id=user_id).update(last_name=last_name)
