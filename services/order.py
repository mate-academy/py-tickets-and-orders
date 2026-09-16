import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: datetime.datetime = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.refresh_from_db()

    for ticket in tickets:
        Ticket.objects.create(row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session=get_movie_session_by_id(
                                  ticket["movie_session"]),
                              order=order)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
