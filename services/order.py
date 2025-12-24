from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(
        user=user
    )
    if date:
        try:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            order.created_at = created_at
        except ValueError:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = created_at

    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
