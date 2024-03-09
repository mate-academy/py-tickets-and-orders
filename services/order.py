from db.models import Ticket, Order, MovieSession
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    order.save()

    for ticket in tickets:
        row, seat, movie_session_id = ticket.values()
        movie_session = MovieSession.objects.get(pk=movie_session_id)
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        return orders.filter(user=user)
    return orders
