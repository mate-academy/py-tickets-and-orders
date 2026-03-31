from db.models import Ticket, Order, MovieSession
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order | None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        ticket_objects = [
            Ticket(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
