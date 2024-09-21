from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date

        order.save()

        tickets_obj = [
            Ticket(
                order=order,
                movie_session=MovieSession.objects.get(
                    pk=ticket["movie_session"]
                ),
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(tickets_obj)

        return order


def get_orders(username: str = None) -> QuerySet:
    with transaction.atomic():
        orders = Order.objects.all()

        if username:
            orders = Order.objects.filter(user__username=username)

    return orders
