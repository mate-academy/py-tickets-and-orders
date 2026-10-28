from django.contrib.auth import get_user_model


user_model = get_user_model()


def create_user(username: str, password: str,
                email: str = None, first_name: str = None,
                last_name: str = None) -> user_model:
    names_dict = {}
    if first_name:
        names_dict["first_name"] = first_name
    if last_name:
        names_dict["last_name"] = last_name
    user = user_model.objects.create_user(username=username,
                                          password=password,
                                          email=email, **names_dict)
    return user


def get_user(user_id: int) -> user_model:
    return user_model.objects.get(pk=user_id)


def update_user(user_id: int,
                password: str = None,
                username: str = None, email: str = None,
                first_name: str = None,
                last_name: str = None) -> user_model:
    user = user_model.objects.get(pk=user_id)
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if password:
        user.set_password(raw_password=password)
    user.save()
    return user
