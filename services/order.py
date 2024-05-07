from django.db.models import QuerySet

from datetime import datetime

from db.models import Order, Ticket


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    pass


def get_orders(username: str = None) -> QuerySet(Order):
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
