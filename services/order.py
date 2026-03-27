from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    order = Order(
        user=get_user_model().objects.get(username=username),
    )
    order.save()

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    movie_session = MovieSession.objects.get(pk=tickets[0]["movie_session"])

    tickets = Ticket.objects.bulk_create(
        [
            Ticket(
                row=ticket_dict["row"],
                seat=ticket_dict["seat"],
                movie_session=movie_session,
                order=order,
            )
            for ticket_dict in tickets
        ]
    )

    order.tickets.set(tickets)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
