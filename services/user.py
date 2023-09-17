from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


def create_user(username, password, email=None, first_name=None, last_name=None):

    try:
        user = User.objects.get(username=username)
        return None
    except ObjectDoesNotExist:
        pass

    user = User(
        username=username,
        password=make_password(password),
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()
    return user


def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    try:
        user = User.objects.get(pk=user_id)
        if username is not None:
            user.username = username
        if password is not None:
            user.password = make_password(password)
        if email is not None:
            user.email = email
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.save()
        return user
    except ObjectDoesNotExist:
        return None


def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return None
