from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        if date:
            order = Order.objects.create(
                user=user,
                created_at=date,
            )
        else:
            order = Order.objects.create(
                user=user,
            )

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)

    return Order.objects.all()
