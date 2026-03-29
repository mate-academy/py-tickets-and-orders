from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects
            .get(pk=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
    order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
