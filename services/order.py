from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        movie_session = MovieSession.objects.get(
            pk=ticket["movie_session"]
        )

        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
