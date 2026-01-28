from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        new_order = Order.objects.create(user=user)

        if date:
            Order.objects.filter(
                pk=new_order.pk
            ).update(
                created_at=datetime.strptime(
                    date, "%Y-%m-%d %H:%M"
                )
            )

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=new_order,
            )


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
