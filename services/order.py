from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order
from db.models import Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:

    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order(user=user)
        order.save()

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            ticket = Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            ticket.save()


def get_orders(username: str = None) -> Order:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
