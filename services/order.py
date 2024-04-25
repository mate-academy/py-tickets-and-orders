from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Ticket, Order


@transaction.atomic()
def create_order(tickets: list[Ticket],
                 username: str,
                 date: datetime = None,
                 ) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order_id=order.id,
            seat=ticket["seat"],
            row=ticket["row"]
        )


def get_orders(username: str = None) -> list[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
