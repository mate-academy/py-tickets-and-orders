from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: dict,
        username: str,
        date: datetime | None = None
) -> Order:
    user = User.objects.get(username=username)

    order_data = {
        "user": user,
    }

    if date is not None:
        order_data["created_at"] = date

    order = Order.objects.create(**order_data)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
