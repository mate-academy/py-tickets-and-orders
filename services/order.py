import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: datetime = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(movie_session=movie_session,
                              row=ticket["row"],
                              seat=ticket["seat"],
                              order=order)
    if date:
        order.created_at = date
        order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
