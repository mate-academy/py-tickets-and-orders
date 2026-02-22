from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import User, Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None
) -> Order:

    user = User.objects.get(username=username)
    if date:
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save()
    else:
        order = Order.objects.create(user=user)

    obj_tickets = []
    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        obj_ticket = Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
            order=order
        )
        obj_tickets.append(obj_ticket)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
