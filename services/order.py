from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractBaseUser

from db.models import Order, Ticket

User = get_user_model()


def get_user(username: str) -> AbstractBaseUser:
    return User.objects.get(username=username)


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
