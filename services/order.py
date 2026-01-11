from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession
from typing import Optional


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None,
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username),
    )
    if date:
        order.created_at = date
    order.save()
    objects_list = [
        Ticket(
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(objects_list)
    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        return orders.filter(user__username=username)
    return orders
