from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:

    user = User.objects.get(username=username)

    new_order = Order.objects.create(
        user=user
    )

    if date is not None:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=new_order
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    query_set = Order.objects.all()
    if username:
        query_set = query_set.filter(user__username=username)
    return query_set
