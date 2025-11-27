import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: Optional[datetime.datetime] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])
    for ticket in tickets:
        ms = MovieSession.objects.get(pk=ticket["movie_session"])
        Ticket.objects.create(
            order=order,
            movie_session=ms,
            row=ticket["row"],
            seat=ticket["seat"])
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.select_related("user").order_by("-created_at")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
