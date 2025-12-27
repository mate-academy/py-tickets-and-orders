from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]

            Ticket.objects.create(
                order=order,
                movie_session_id=movie_session_id,
                row=row,
                seat=seat
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(
            user__username=username
        )

    return orders
