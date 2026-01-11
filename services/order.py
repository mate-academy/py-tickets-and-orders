from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        order = Order.objects.create(
            user=user,
        )

        if date:
            order.created_at = date
        order.save()

        tickets_objs = Ticket.objects.bulk_create(
            Ticket(
                row=ticket["row"], seat=ticket["seat"],
                movie_session_id=ticket["movie_session"], order=order
            )
            for ticket in tickets
        )
        for ticket_obj in tickets_objs:
            ticket_obj.clean()


def get_orders(username: str = None) -> list[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(
            user=get_user_model().objects.get(username=username)
        )
    return orders
