from django.db.models import QuerySet

from db.models import Order, Ticket, User
from datetime import datetime
from django.db import transaction


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(
        user=user
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username__icontains=username)
    return Order.objects.all()
