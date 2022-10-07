from django.contrib.auth import get_user_model

import init_django_orm  # noqa: F401

from db.models import User


def create_user(username, password, email=None, first_name=None, last_name=None):
    user = get_user_model().objects.create_user(
      username=username, password=password, email=email, first_name=first_name,
      last_name=last_name
    )
    return user


def get_user(user_id):
    user_ = get_user_model().objects.get(id=user_id)
    return user_


def update_user(user_id, username=None, password=None, email=None,
                first_name=None, last_name=None):
    user_ = get_user(user_id)
    if password:
        user_.set_password = password
    if username:
        user_.username = username
    if email:
        user_.email = email
    if first_name:
        user_.first_name = first_name
    if last_name:
        user_.last_name = last_name
    user_.save()
    return user_


if __name__ == '__main__':
    pass

