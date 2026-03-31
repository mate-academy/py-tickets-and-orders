from datetime import datetime
from typing import List, Any

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, User, Order, MovieSession


@transaction.atomic
def create_order(tickets: List[dict[str, Any]],
                 username: str,
                 date: datetime = None
                 ) -> List[Ticket]:
    ticket_objects = []
    user, created = User.objects.get_or_create(username=username)
    order = Order.objects.create(user=user, created_at=date)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        try:
            movie_session = (
                MovieSession.objects.get(id=ticket["movie_session"]))
        except MovieSession.DoesNotExist:
            raise (
                ValueError
                (f"MovieSession "
                 f"with id {ticket['movie_session']} does not exist")
            )
        ticket_objects.append(Ticket(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        ))
    return Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(
            user__username=username).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
