from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
    tickets: list[dict], username: str, date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        new_order = Order.objects.create(user=user)

        if date:
            new_order.created_at = date
            new_order.save()

        tickets = [
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=new_order,
            )
            for ticket in tickets
        ]

        for ticket in tickets:
            ticket.save()

        return new_order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
