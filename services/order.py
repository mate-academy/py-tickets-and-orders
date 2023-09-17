from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(created_at=date, user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
