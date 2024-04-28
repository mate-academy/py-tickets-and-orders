from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


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

    movie_session = MovieSession.objects.get(pk=tickets[0]["movie_session"])
    Ticket.objects.bulk_create(
        [
            Ticket(row=ticket["row"],
                   seat=ticket["seat"],
                   movie_session=movie_session,
                   order=order)
            for ticket in tickets
        ]
    )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    queryset = queryset.filter(
        user__username=username
    ) if username else queryset
    return queryset
