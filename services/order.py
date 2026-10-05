from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date is not None:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username is not None:
        orders = orders.filter(user__username=username)

    return orders
