from django.contrib.auth import get_user_model

from db.models import User


def create_user(username: str,
                password: str,
                **kwargs) -> None:
    get_user_model().objects.create_user(
        username=username,
        password=password,
    )
    get_user_model().objects.filter(username=username).update(**kwargs)


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, password: str = None, **kwargs) -> User:
    user_to_update = get_user_model().objects.filter(id=user_id)
    if kwargs:
        user_to_update.update(**kwargs)
    if password:
        user_to_update = user_to_update.get(id=user_id)
        user_to_update.set_password(password)
        user_to_update.save()
    return user_to_update
