from django.db import transaction
from django.db.models import QuerySet
from django.db.models.fields import DateTimeField

from db.models import Order, Ticket, User


def create_order(tickets: list[dict], username: str,
                 date: DateTimeField = None) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
