import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
    )
    if date:
        order.created_at = datetime.datetime.strptime(
            date,
            "%Y-%m-%d %H:%M"
        )
        order.save()
    tickets_objects = [
        Ticket(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        ) for ticket in tickets
    ]
    for ticket in tickets_objects:
        ticket.clean()

    Ticket.objects.bulk_create(tickets_objects)


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
