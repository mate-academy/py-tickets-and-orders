from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    pass


def get_user(user_id: int) -> User:
    return User.objects.get(user_id=user_id)


def update_user(
        user_id: int,
        usename: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:
    pass
