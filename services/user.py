from django.contrib.auth import get_user_model


def create_user(username, password, email = None, first_name = None, last_name = None):
    get_user_model().objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

def get_user(user_id):
    return get_user_model().objects.get(pk=user_id)

def update_user(user_id, username = None, password = None, email = None, first_name = None, last_name = None):
    if username:
        get_user(user_id=user_id).username = username
    if password:
        get_user(user_id=user_id).set_password(password)
    if email:
        get_user(user_id=user_id).email = email
    if first_name:
        get_user(user_id=user_id).first_name = first_name
    if last_name:
        get_user(user_id=user_id).last_name = last_name
