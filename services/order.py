from typing import List, Optional


from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic()
def create_order(tickets: List[dict],
                 username: str,
                 date: Optional[str] = None) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))
    if date:
        order.created_at = date
        order.save()

    for new_ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=new_ticket.get("movie_session"),
            row=new_ticket.get("row"),
            seat=new_ticket.get("seat")
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
