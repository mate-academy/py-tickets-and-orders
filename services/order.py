from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    created_at = parse_datetime(date) if date else None
    order = Order.objects.create(user=user)

    if created_at:
        order.created_at = created_at
        order.save()

    for ticket in tickets:
        movie_session_id = ticket["movie_session"]
        movie_session = MovieSession.objects.get(id=movie_session_id)
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
