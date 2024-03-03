from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username,
                password,
                email=None,
                first_name=None,
                last_name=None):
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name)
    return user


def get_user(user_id):
    return User.objects.get(id=user_id)


def update_user(
        user_id,
        username=None,
        password=None,
        email=None,
        first_name=None,
        last_name=None):
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
    return user
