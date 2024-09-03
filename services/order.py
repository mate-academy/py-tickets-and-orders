from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )


def get_orders(username: str = None) -> list[Order]:
    if username is None:
        return Order.objects.all()
    user = User.objects.get(username=username)
    orders = Order.objects.filter(user=user)
    return orders
