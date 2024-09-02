from django.db import transaction

from db.models import Order, User, MovieSession
from db.models import Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None,
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

    return order


def get_orders(username: str | None = None) -> list[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders.order_by("-created_at")
