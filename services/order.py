from db.models import Order, Ticket, MovieSession, User
from django.db import transaction
from django.db.models.query import QuerySet
from typing import Optional


@transaction.atomic()
def create_order(
    tickets: list[dict],
    username: str,
    date: Optional[str] = None,
) -> Order:

    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        ticket = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=movie_session,
            order=order)
        ticket.save()
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
