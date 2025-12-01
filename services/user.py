from db.models import User


def create_user(username: str, password: str, email: str = None,
                first_name: str = None, last_name: str = None) -> User:
    us = User.objects.create_user(username=username, password=password,
                             email=email)
    if first_name is not None:
        us.first_name = first_name
        us.save()
    if last_name is not None:
        us.last_name = last_name
        us.save()
    # if email:
    #     us.email = email
    # if first_name:
    #     us.first_name = first_name
    # if last_name:
    #     us.last_name = last_name
    # us.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int, username: str = None,
                password: str = None, email: str = None,
                first_name: str = None, last_name: str = None) -> User:
    us = User.objects.get(id=user_id)
    if username is not None:
        us.username = username
    if password is not None:
        us.set_password(password)
    if email is not None:
        us.email = email
    if first_name is not None:
        us.first_name = first_name
    if last_name is not None:
        us.last_name = last_name
    us.save()
