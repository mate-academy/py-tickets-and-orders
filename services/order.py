import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    user = get_user_model().objects.get(username=username)

    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
