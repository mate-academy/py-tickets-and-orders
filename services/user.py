from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    user = User.objects.create_user(
        username=username,
        password=password,
    )
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None :
    user = User.objects.get(id=user_id)
    for key, value in kwargs.items():
        if key == "password":
            user.set_password(value)
            continue
        setattr(user, key, value)
    user.save()
