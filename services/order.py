from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for num_seat in tickets:
            Ticket.objects.create(
                movie_session_id=num_seat["movie_session"],
                order=order,
                row=num_seat["row"],
                seat=num_seat["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all().order_by("-id")

    if username:
        orders = orders.filter(user__username=username)

    return orders
