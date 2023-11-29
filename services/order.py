from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.query import QuerySet
from db.models import Ticket, Order, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        customer_user = get_user_model().objects.get(username=username)
        user_order = Order.objects.create(user=customer_user)

        if date:
            user_order.created_at = date
            user_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=user_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
