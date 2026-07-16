from django.contrib.auth import get_user_model


def get_user(user_id: int):
    return get_user_model().objects.get(id=user_id)


def create_user(**extra_fields):
    return get_user_model().objects.create_user(**extra_fields)


def update_user(user_id: int, **extra_fields) -> None:
    user = get_user(user_id)
    if "password" in extra_fields:
        user.set_password(extra_fields.pop("password"))
    for field, value in extra_fields.items():
        setattr(user, field, value)
    user.save()
