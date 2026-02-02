from django.contrib.auth import get_user_model
from db.models import User


def create_user(username: str, password: str, **kwargs) -> User:
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username=username,
        password=password,
        **{k: v for k, v in kwargs.items() if v is not None}
    )
    return user


def get_user(user_id: int) -> User:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs) -> None:
    user = get_user(user_id)
    if "password" in kwargs:
        user.set_password(kwargs["password"])
    for key, value in kwargs.items():
        if key == "password":
            continue
        if value is not None:
            setattr(user, key, value)
    user.save()
