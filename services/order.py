from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()
        [Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))
    return Order.objects.all()
