from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db.transaction import atomic

from db.models import Ticket, Order
from services.movie_session import get_movie_session_by_id


@atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:

    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    Ticket.objects.bulk_create(
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=get_movie_session_by_id(ticket["movie_session"]),
            order_id=order.id
        ) for ticket in tickets
    )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)
    return orders
