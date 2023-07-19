from django.contrib.auth import get_user_model
from db.models import Ticket, Order
from django.db import transaction
from django.db.models import QuerySet


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    order = Order.objects.all()

    if username:
        order = order.filter(user__username=username)

    return order
