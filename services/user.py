from db.models import User


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str = None,
                last_name: str = None):
    new_user = User.objects.create_user(username=username, password=password)
    user = User.objects.filter(id=new_user.id)
    if email:
        user.update(email=email)
    if first_name:
        user.update(first_name=first_name)
    if last_name:
        user.update(last_name=last_name)


def get_user(user_id: int):
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str = None,
                password: any = None,
                email: str = None,
                first_name: str = None,
                last_name: str = None):
    user = User.objects.filter(id=user_id)

    if username:
        user.update(username=username)
    if password:
        user_with_new_password = User.objects.get(id=user_id)
        user_with_new_password.set_password(password)
        user_with_new_password.save()
    if email:
        user.update(email=email)
    if first_name:
        user.update(first_name=first_name)
    if last_name:
        user.update(last_name=last_name)
