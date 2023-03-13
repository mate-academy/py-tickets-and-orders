from db.models import Order, Ticket, User
from django.db import transaction


def create_order(tickets: list[dict], username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        for ticket in tickets:
            Ticket.objects.create(order=order, **ticket)

        if date:
            order.created_at = date
            order.save()


def get_orders(username=None):
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders

