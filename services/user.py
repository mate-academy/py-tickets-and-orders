from django.contrib.auth import get_user_model

from db.models import User

from support.validators import table_item_exist


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "") -> User:
    user = get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user


def get_user(user_id: int) -> User | None:
    if table_item_exist(get_user_model(), user_id):
        return get_user_model().objects.get(id=user_id)
    print(f"The user with the specified id: {user_id} doesn't exist!")


def update_user(user_id: int,
                username: str | None = None,
                password: str | None = None,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None) -> None:
    user = get_user(user_id)
    if user:
        if password:
            user.set_password(password)
        fields = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name}
        for field, new_info in fields.items():
            user_attr = user.__getattribute__(field)
            if new_info and new_info != user_attr:
                user.__setattr__(field, new_info)
        user.save()
