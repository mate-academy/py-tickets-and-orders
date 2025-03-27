from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    tickets_for_order = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session_id"],
            order=order,
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(tickets_for_order)

    return order


def get_user_orders(username: str) -> QuerySet[Order]:
    user = User.objects.get(username=username)
    return Order.objects.filter(user=user)
