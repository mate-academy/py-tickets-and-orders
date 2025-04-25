from typing import Optional

from db.models import User


def create_user(
        username: str,
        password: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> User:
    create_user_dict = {}
    if email:
        create_user_dict["email"] = email
    if first_name:
        create_user_dict["first_name"] = first_name
    if last_name:
        create_user_dict["last_name"] = last_name

    return User.objects.create_user(username=username,
                                    password=password,
                                    **create_user_dict)


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: Optional[str] = None,
                password: Optional[str] = None,
                email: Optional[str] = None,
                first_name: Optional[str] = None,
                last_name: Optional[str] = None) -> User:
    user = User.objects.get(id=user_id)
    user_dict = {}

    if username:
        user_dict["username"] = username
    if password:
        user_dict["password"] = password
    if email:
        user_dict["email"] = email
    if first_name:
        user_dict["first_name"] = first_name
    if last_name:
        user_dict["last_name"] = last_name

    for key, value in user_dict.items():
        if key != "password":
            setattr(user, key, value)
    if password:
        user.set_password(password)

    user.save()
    return user
