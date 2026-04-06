from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

from django.db import transaction


@transaction.atomic
def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])
    for item in tickets:
        Ticket.objects.create(
            movie_session_id=item["movie_session"],
            order=order,
            row=item["row"],
            seat=item["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
