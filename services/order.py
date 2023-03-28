import datetime
from typing import Optional, List

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: List[dict],
                 username: Optional[str] = None,
                 date: Optional[str] = None) -> Order:
    user = User.objects.get(username=username)
    if date is not None:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user)
        order.created_at = date
        order.save()
    else:
        date = datetime.datetime.strptime(
            date, "%Y-%m-%d %H:%M"
        ) if date is not None else None
        order = Order.objects.create(user=user, created_at=date)

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
