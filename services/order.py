from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save(update_fields=["created_at"])
    for ticket in tickets:
        ticket_data = ticket.copy()
        ticket_data["movie_session_id"] = ticket_data.pop("movie_session")
        Ticket.objects.create(order=order, **ticket_data)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
