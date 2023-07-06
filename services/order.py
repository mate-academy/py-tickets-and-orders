import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


@transaction.atomic()
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime.date = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    tickets_list = [Ticket(
        movie_session=MovieSession.objects.get(
            movie_id=ticket["movie_session"]
        ),
        order=order,
        row=ticket["row"],
        seat=ticket["seat"]
    ) for ticket in tickets]
    Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> Order:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
