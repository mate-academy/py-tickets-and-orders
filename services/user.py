from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username: str,
                password: str,
                email: str = None,
                first_name: str | None = None,
                last_name: str | None = None,
                ) -> User:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password)
    return user


def get_user(user_id: int) -> User:
    user = User.objects.get(pk=user_id)
    return user


def update_user(user_id: int,
                username: str | None = None,
                email: str | None = None,
                password: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None,
                ) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
