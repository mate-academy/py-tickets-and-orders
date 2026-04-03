import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Ticket, Order


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None,
) -> Order:
    tickets_instances = []
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        tickets_instances.append(
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        )

    Ticket.objects.bulk_create(tickets_instances)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
