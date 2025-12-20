from django.contrib.auth import get_user_model


def create_user(**kwargs) -> get_user_model():
    return get_user_model().objects.create_user(**kwargs)


def get_user(user_id: int) -> get_user_model():
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> get_user_model():
    user = get_user_model().objects.get(id=user_id)
    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))
    for field, value in kwargs.items():
        setattr(user, field, value)
    user.save()
    return user
