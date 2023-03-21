from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        new_order = Order.objects.create(user=user)
        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.all().filter(user__username=username)
    return Order.objects.all()
