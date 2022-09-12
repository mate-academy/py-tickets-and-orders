from db.models import User


def create_user(username, password, email=None,
                first_name=None, last_name=None):
    user = User.objects.create_user(username, email, password)
    if first_name:
        user.first_name = first_name
        user.save()
    if last_name:
        user.last_name = last_name
        user.save()


def get_user(user_id):
    return User.objects.get(id=user_id)


def update_user(user_id, username=None, password=None,
                email=None, first_name=None, last_name=None):
    if username:
        User.objects.filter(id=user_id).update(username=username)
    if email:
        User.objects.filter(id=user_id).update(email=email)
    if password:
        u = User.objects.get(id=user_id)
        u.set_password(password)
        u.save()
    if first_name:
        User.objects.filter(id=user_id).update(first_name=first_name)
    if last_name:
        User.objects.filter(id=user_id).update(last_name=last_name)
