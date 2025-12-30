from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    new_order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        new_order.created_at = datetime.strptime(
            date,
            "%Y-%m-%d %H:%M"
        )

    new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=new_order,
            movie_session=MovieSession.objects.get(
                id=ticket.get("movie_session")
            ),
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(
            user=get_user_model().objects.get(username=username)
        )

    return queryset
