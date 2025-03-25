from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


USER = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        customer = USER.objects.get(username=username)

        new_order = Order.objects.create(user=customer)
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=new_order
            )

        return new_order


def get_orders(
        username: str = None
) -> QuerySet:
    orders = Order.objects.all()

    if username:
        user = USER.objects.get(username=username)
        orders = orders.filter(user=user)

    return orders
