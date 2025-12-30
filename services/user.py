from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet


def get_user_by_username(username: str) -> Any:
    return get_user_model().objects.get(username=username)


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Any:
    user_model = get_user_model()
    extra_fields: dict[str, Any] = {}
    if email is not None:
        extra_fields["email"] = email
    if first_name is not None:
        extra_fields["first_name"] = first_name
    if last_name is not None:
        extra_fields["last_name"] = last_name
    return user_model.objects.create_user(
        username=username,
        password=password,
        **extra_fields,
    )


def get_users() -> QuerySet:
    return get_user_model().objects.all().order_by("username")


def get_user(user_id: int) -> Any:
    return get_user_model().objects.get(id=user_id)


def update_user(user_id: int, **kwargs: Any) -> Any:
    user = get_user(user_id)
    if "password" in kwargs:
        user.set_password(kwargs.pop("password"))
    for attr, value in kwargs.items():
        setattr(user, attr, value)
    user.save()
    return user
