import datetime

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(pk=order.id).update(created_at=date)

    list_id = [
        ticket["movie_session"] for ticket in tickets
    ]
    movie_sessions = MovieSession.objects.in_bulk(list_id)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=movie_sessions[ticket["movie_session"]],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
