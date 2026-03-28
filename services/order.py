from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order


def create_order(tickets: list[dict],
                 username: str,
                 date = None):
    if date:
        with transaction.atomic():
            #order = Order.objects.create(user__username=username,
                                         #created_at=date)
            Order.objects.create(user_id=user.id, created_at=date)
            for ticket in tickets:
                Ticket.objects.create(order=order,
                                      **ticket)
            return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
        return orders
    else:
        orders = Order.objects.all()
        return orders
