from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Ticket, Order
from django.db.models import DateTimeField, QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: DateTimeField = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet:
    if username:

        return Order.objects.filter(user__username=username)

    return Order.objects.all()
