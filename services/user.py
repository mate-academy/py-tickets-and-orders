from db.models import User


def create_user(username: str, password: str, email: str = None, first_name: str = None, last_name: str = None):
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return user

def get_user(user_id: int):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None   

def update_user(user_id: int, username: str = None, password: str = None, email: str = None, first_name: str = None, last_name: str = None):
    try:
        user = User.objects.get_user(id=user_id)

        if username:
            user.username = username
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)

        user.save()
        return user
    except User.DoesNotExist:
        return None