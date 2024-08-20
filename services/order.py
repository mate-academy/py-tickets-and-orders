from django.db import transaction
from django.utils import timezone

from db.models import Order, Ticket, User

from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    if not date:
        date = timezone.now()

    order = Order.objects.create(
        user=user,
        created_at=date
    )

    ticket_objects = []
    for ticket_data in tickets:
        ticket = Ticket(
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            order=order
        )
        ticket_objects.append(ticket)

    Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
