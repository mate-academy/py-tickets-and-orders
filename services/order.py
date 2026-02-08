from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.db.models.functions import datetime
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = parse_datetime(date)
        order.save()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session,
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
