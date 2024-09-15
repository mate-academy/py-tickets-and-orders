from db.models import Ticket, Order
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction


@transaction.atomic()
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
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session_id = ticket["movie_session"]

        Ticket.objects.create(
            order=order,
            movie_session_id=movie_session_id,
            row=row,
            seat=seat
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(user=user)

    return orders
