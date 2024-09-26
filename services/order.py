from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    new_order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        new_ticket = Ticket()
        new_ticket.row = ticket.get("row")
        new_ticket.seat = ticket.get("seat")
        new_ticket.movie_session_id = ticket.get("movie_session")
        new_ticket.order = new_order
        new_ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
