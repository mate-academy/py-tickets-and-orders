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

        Ticket.objects.bulk_create(
            [Ticket(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"]
            ) for ticket in tickets
            ]
        )

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.prefetch_related("user")

    if username:
        orders = orders.filter(user__username=username)

    return orders
