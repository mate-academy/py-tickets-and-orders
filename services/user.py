from django.contrib.auth import get_user_model
from django.db.models import Model


def create_user(
        username: str,
        password: str,
        email: str = None,
        # Change default from None to "" to prevent DB integrity errors
        first_name: str = "",
        last_name: str = "",
) -> Model:
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    return user


def get_user(user_id: int) -> Model:
    user_model = get_user_model()
    return user_model.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
) -> None:
    # Refactored: Reuse the existing get_user function
    user = get_user(user_id)

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
