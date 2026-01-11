from django.shortcuts import get_object_or_404

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:

    user = get_object_or_404(User, username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: str = None) -> QuerySet:

    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
