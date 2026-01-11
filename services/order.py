import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    ticket_objects = []
    for ticket in tickets:
        movie_session_id = ticket["movie_session"]
        movie_session = MovieSession.objects.get(id=movie_session_id)
        ticket_ = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
            movie_session=movie_session
        )
        ticket_objects.append(ticket_)

    Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> Order:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
