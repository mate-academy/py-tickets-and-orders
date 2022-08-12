from django.contrib.auth import get_user_model

from db.models import User


def create_user(username,
                password,
                email=None,
                first_name=None,
                last_name=None):
    user = get_user_model().objects.create_user(
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


def get_user(user_id):

    return get_user_model().objects.get(id=user_id)


def update_user(user_id,
                username=None,
                password=None,
                email=None,
                first_name=None,
                last_name=None):
    user_to_update = User.objects.get(id=user_id)
    if username:
        user_to_update.username = username
    if password:
        user_to_update.set_password(password)
    if email:
        user_to_update.email = email
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name

    user_to_update.save()
