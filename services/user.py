from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


def create_user( username, password, user_id=None, email=None, first_name=None, last_name=None):
    try:
        user, created = User.objects.update_or_create(id=user_id, defaults={'username': username, 'password': make_password(password)})
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return user
    except User.DoesNotExist:
        return None


def get_user(user_id):
    return User.objects.get(id=user_id)

def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

    if username is not None:
        user.username = username
    if password is not None:
        user.set_password(password)
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    user.save()
    return user

