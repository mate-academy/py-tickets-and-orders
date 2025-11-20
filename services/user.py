from django.contrib.auth import get_user_model

UserModel = get_user_model()


def create_user(
        username: str,
        password: str,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> UserModel:
    extra = {}
    if first_name:
        extra["first_name"] = first_name
    if last_name:
        extra["last_name"] = last_name

    return UserModel.objects.create_user(
        username=username, password=password, email=email, **extra
    )


def get_user(user_id: int) -> UserModel | None:
    try:
        return UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        return None


def update_user(
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
) -> UserModel:
    user = get_user(user_id)
    if not user:
        return None

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
