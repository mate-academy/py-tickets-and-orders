from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None,
) -> Order:
    new_tickets = []
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
    )
    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
    for ticket in tickets:
        new_ticket = Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        new_ticket.full_clean()
        new_tickets.append(new_ticket)
    Ticket.objects.bulk_create(new_tickets)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
