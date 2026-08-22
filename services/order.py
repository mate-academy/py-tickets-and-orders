from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime | str | None = None
) -> None:
    user = get_user_model().objects.get(username=username)

    if date and isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    order = Order.objects.create(user=user)

    if date:
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
