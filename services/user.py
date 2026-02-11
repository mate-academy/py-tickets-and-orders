from db.models import User


def create_user(username, password, email=None, first_name=None, last_name=None):
    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id):
    return User.objects.get(id=user_id)


def update_user(user_id, username=None, password=None, email=None, first_name=None, last_name=None):
    user = User.objects.get(id=user_id)
    if username:
        user.username = username
    if password:
        user.set_password(password)
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    return user
