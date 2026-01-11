from db.models import User


from django.db.models import QuerySet


def create_user(
        password: str,
        username: str,
        first_name: str = "",
        last_name: str = "",
        email: str = ""
) -> User:

    return User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )


def get_user(user_id: int) -> User:
    if user_id is None:
        return None
    else:
        return User.objects.filter(id=user_id).first()


def update_user(
    user_id: int,
    email: str | None = None,
    password: str | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None
) -> QuerySet[User]:
    user = get_user(user_id)
    if user is None:
        return None

    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email:
        user.email = email
    if password:
        user.set_password(password)

    user.save()

    return user
