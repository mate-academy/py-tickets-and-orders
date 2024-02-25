from db.models import User


def create_user(username: str,
                password: str,
                email: str = "",
                first_name: str = "",
                last_name: str = "",
                ) -> None:
    user = User.objects.create_user(username=username,
                                    password=password)

    user.email = email
    user.first_name = first_name
    user.last_name = last_name

    user.save()


def get_user(user_id: int, ) -> User:
    return User.objects.get(id=user_id)


def update_user(user_id: int,
                username: str | None = None,
                password: str | None = None,
                email: str | None = None,
                first_name: str | None = None,
                last_name: str | None = None,
                ) -> None:
    user = get_user(user_id)

    if password:
        user.set_password(password)

    for field, value in (("username", username),
                         ("email", email),
                         ("first_name", first_name),
                         ("last_name", last_name)):
        if value:
            setattr(user, field, value)

    user.save()


def delete_user(user_id: int, ) -> None:
    User.objects.get(user_id=user_id).delete()
