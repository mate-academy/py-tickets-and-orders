from __future__ import annotations

from django.contrib.auth.models import UserManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models import User


class CustomUserManager(UserManager):

    def create_user_with_optional(
        self,
        username: str,
        password: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> "User":
        user = self.create_user(username=username, password=password)

        if email is not None:
            user.email = email

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        user.save()
        return user
