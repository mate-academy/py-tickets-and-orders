from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    user = User.objects.create_user(username=username, password=password)

    if email:
        user.email = email
        user.save()
    if first_name:
        user.first_name = first_name
        user.save()
    if last_name:
        user.last_name = last_name
        user.save()
    return user


def get_user(user_id: str) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: str,
                username: str = None,
                password: str = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None) -> User:
    new_user = User.objects.get(id=user_id)
    if username:
        new_user.username = username
    if password:
        new_user.set_password(password)
    if email:
        new_user.email = email
    if first_name:
        new_user.first_name = first_name
    if last_name:
        new_user.last_name = last_name
    new_user.save()
    return new_user
