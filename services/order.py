from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
    order.save()

    for ticket in tickets:
        movie_session_instance = MovieSession.objects.get(
            id=ticket["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            movie_session=movie_session_instance,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


@transaction.atomic
def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username is not None:
        return orders.filter(user__username=username)
    return orders
