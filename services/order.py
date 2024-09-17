from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order_id=order.id
        )

    order.save()


def get_orders(username: str = None) -> Order:
    order = Order.objects.all()

    if username:
        order = Order.objects.filter(user__username=username)

    return order
