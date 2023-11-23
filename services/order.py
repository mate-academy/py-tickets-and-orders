import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    if date:
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save()
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        movie_session_id = ticket_data["movie_session"]
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        if row is not None and seat is not None:
            movie_session = MovieSession.objects.get(pk=movie_session_id)
            ticket = Ticket(
                order=order,
                movie_session=movie_session,
                row=row,
                seat=seat
            )
            ticket.full_clean()
            ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
