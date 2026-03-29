from datetime import datetime
from db.models import Order, User, Ticket
from django.db.models import QuerySet
from django.db import transaction


def create_order(tickets: list,
                 username: str,
                 date: datetime = None) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date

        for ticket in tickets:
            ticket_ = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order)
            ticket_.save()

        order.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
