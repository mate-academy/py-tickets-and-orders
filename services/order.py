
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = get_object_or_404(User, username=username)

    order = Order.objects.create(
        user=user,
    )
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        movie_session = ticket.get("movie_session")

        Ticket.objects.create(
            movie_session_id=movie_session,
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
