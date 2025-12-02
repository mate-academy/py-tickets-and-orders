from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:

    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        parsed_date = parse_datetime(date)
        Order.objects.filter(id=order.id).update(created_at=parsed_date)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
