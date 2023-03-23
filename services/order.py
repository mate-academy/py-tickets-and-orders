from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket



def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None,
) -> Order:

    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            row, seat, movie_session = ticket_data.values()
            Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session_id=movie_session
            )

    return order


def get_orders(username: str = None) -> QuerySet:

    orders = Order.objects.all()

    if username:
        orders = Order.objects.filter(user__username=username)

    return orders
