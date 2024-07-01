from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            ticket = Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=ticket["movie_session"],
                order=order
            )
            ticket.full_clean()
            ticket.save()

        return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders.filter(user__username=username)
    return orders
