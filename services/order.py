from django.db import transaction
from db.models import Ticket, User, Order
from typing import List, Dict


def create_order(tickets: List[Dict], username: str, date: str = None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=ticket["movie_session"]
            )


def get_orders(username: str):
    return Order.objects.filter(user__username__contains=username).order_by('-id')
