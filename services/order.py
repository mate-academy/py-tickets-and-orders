import datetime
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])

    tickets_to_create = [Ticket(
        movie_session_id=ticket["movie_session"],
        order=order,
        row=ticket["row"],
        seat=ticket["seat"]
    ) for ticket in tickets]

    for ticket in tickets_to_create:
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
