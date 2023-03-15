from db.models import User


def create_user(
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:

    creating_queryset = User.objects.create_user(
        username=username,
        password=password,
    )

    if email:
        creating_queryset.email = email

    if first_name:
        creating_queryset.first_name = first_name

    if last_name:
        creating_queryset.last_name = last_name

    creating_queryset.save()


def get_user(user_id: int) -> User:
    return User.objects.get(id=user_id)


def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        email: str = None,
        first_name: str = None,
        last_name: str = None
) -> None:

    updating_queryset = User.objects.get(id=user_id)

    if password:
        updating_queryset.set_password(password)

    if first_name:
        updating_queryset.first_name = first_name

    if last_name:
        updating_queryset.last_name = last_name

    if email:
        updating_queryset.email = email

    if username:
        updating_queryset.username = username

    updating_queryset.save()

    return updating_queryset
