import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        row = ticket_data["row"]
        seat = ticket_data["seat"]

        Ticket.objects.create(
            order=order,
            movie_session_id=movie_session_id,
            row=row,
            seat=seat,
        )
    order.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
