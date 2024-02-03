from django.db import transaction

from db.models import Order, Ticket, User
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:

    with transaction.atomic():

        orders_user = User.objects.get(
            username=username
        )
        new_order = Order.objects.create(
            user=orders_user
        )
        if date:
            new_order.created_at = date

        new_order.save()

        ticket_instances = [
            Ticket(
                order=new_order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_instances)

        return new_order


def get_orders(
    username: str = None
) -> Order:

    orders = Order.objects.all()

    if username:
        orders = Order.objects.filter(
            user__username=username
        )

    return orders
