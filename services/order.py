from typing import List, Optional
from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: List[dict],
    username: str,
    date: Optional[datetime] = None,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(pk=order.pk).update(created_at=date)
        order.refresh_from_db()

    ticket_objs = [
        Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(pk=ticket["movie_session"])
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(ticket_objs)
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = (
        Order.objects.all()
        .select_related("user")
        .prefetch_related("tickets")
    )
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
