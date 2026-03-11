from django.contrib.auth import get_user_model

def create_user(username, password, email=None, first_name=None, last_name=None):
    User = get_user_model()
    kwargs = {"username": username, "password": password}
    if email is not None:
        kwargs["email"] = email
    if first_name is not None:
        kwargs["first_name"] = first_name
    if last_name is not None:
        kwargs["last_name"] = last_name
    return User.objects.create_user(**kwargs)

def get_user(user_id):
    User = get_user_model()
    return User.objects.get(id=user_id)

def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    User = get_user_model()
    user = User.objects.get(id=user_id)
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
