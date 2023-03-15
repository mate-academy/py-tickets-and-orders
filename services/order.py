from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket_info in tickets:
            Ticket.objects.create(
                order=new_order,
                movie_session_id=ticket_info["movie_session"],
                row=ticket_info["row"],
                seat=ticket_info["seat"]
            )

        return new_order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
