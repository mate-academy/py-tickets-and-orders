from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        tickets = [Ticket(order=order, row=data["row"], seat=data["seat"], movie_session_id=data["movie_session"]) for data in tickets]
        Ticket.objects.bulk_create(tickets)
        # for ticket in tickets:
        #     Ticket.objects.create(order=order, row=ticket["row"], seat=ticket["seat"], movie_session_id=ticket["movie_session"])


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
