from datetime import datetime

from django.contrib.auth import get_user_model

from db.models import Order, Ticket
from django.db import transaction
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | None = None
) -> None:
    user = get_user_model().objects.get(username=username)

    order_data = {"user": user}

    order = Order.objects.create(**order_data)

    if date:
        if isinstance(date, str):
            date = datetime.strptime(
                date,
                "%Y-%m-%d %H:%M"
            )
        Order.objects.filter(pk=order.pk).update(created_at=date)

    bulk_tickets = []

    for ticket in tickets:
        ticket_obj = Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        ticket_obj.full_clean()
        bulk_tickets.append(ticket_obj)

    Ticket.objects.bulk_create(bulk_tickets)


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
