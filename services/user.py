from django.core.exceptions import ObjectDoesNotExist

from db.models import User


def create_user(username, password, /, email, first_name, last_name) -> User:
    user = User.objects.create_user(username=username, password=password)

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    user.save()
    return user


def get_user(user_id: int) -> User:
    try:
        return User.objects.get(id=user_id)  # Отримуємо конкретного користувача
    except User.DoesNotExist:
        raise "Some mistake"


def update_user(
        user_id,
        /,
        username,
        password,
        email,
        first_name,
        last_name) -> User:
    try:
        user = User.objects.get(id=user_id)

        if username:
            user.username = username
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        return user
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"User with ID {user_id} does not exist")

