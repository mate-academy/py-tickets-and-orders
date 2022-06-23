import datetime

from django.db import transaction

from db.models import Ticket, Order, User


def create_order(tickets: list[dict], username: str, date: datetime = None):
    with transaction.atomic():
        user = User.objects.get(username=username)

        order_with_date = Order.objects.create(user=user)

        if date is not None:
            order_with_date.created_at = date
            order_with_date.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order_with_date,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None):
    orders = Order.objects.all().order_by("-id")

    if username:
        return orders.filter(user__username=username)

    return orders
