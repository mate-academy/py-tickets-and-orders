from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=(
                    MovieSession.objects
                    .get(id=ticket["movie_session"])
                ),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> list[dict]:
    order = Order.objects.all()
    if username:
        return order.filter(user__username=username)
    return order
