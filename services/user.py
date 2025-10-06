from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> User:
    user = User.objects.create_user(
        username=username,
        password=User.set_password(password),
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user

def get_user():
    pass

def update_user():
    pass
