from __future__ import annotations

from typing import Any, Optional

from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(
    username: str,
    password: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> Any:
    """
    Cria um usuário usando o manager padrão (create_user),
    garantindo que o password seja corretamente hashado.
    """
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email or "",
        first_name=first_name or "",
        last_name=last_name or "",
    )
    return user


def get_user(user_id: int) -> Any:
    """Retorna um usuário pelo id."""
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> "User":
    """
    Atualiza campos opcionais do usuário.
    Se password for informado, usa set_password para re-hash.
    """
    user = get_user(user_id=user_id)
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name

    if password is not None:
        user.set_password(password)

    user.save()
    return user
