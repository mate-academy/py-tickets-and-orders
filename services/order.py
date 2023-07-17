from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket
from .movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    Ticket.objects.bulk_create(
        Ticket(
            order_id=order.id,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=get_movie_session_by_id(ticket["movie_session"])
        ) for ticket in tickets
    )

    if date:
        order.created_at = date
    order.save()


def get_orders(username: str = None) -> None:
    orders = Order.objects.all()

    if username:
        orders = Order.objects.filter(user__username=username)

    return orders
