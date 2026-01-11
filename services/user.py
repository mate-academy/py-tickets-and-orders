from django.contrib.auth import get_user_model

from db.models import User as UserTyping

UserModel: UserTyping = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str = "",
        first_name: str = "",
        last_name: str = "",
) -> UserModel:
    user = UserModel.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(
        user_id: int
) -> UserModel:
    return UserModel.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> UserModel:
    arguments = locals()
    update_dict = {}
    password = arguments.pop("password")
    for key, value in arguments.items():
        if key == "user_id":
            continue
        if value is not None:
            update_dict[key] = value
    UserModel.objects.filter(id=user_id).update(**update_dict)
    user = UserModel.objects.get(id=user_id)
    if password:
        user.set_password(password)
    user.save()
    return user
