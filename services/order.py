from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(
            seat=ticket["seat"],
            row=ticket["row"],
            movie_session=movie_session,
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)
    return orders
