from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user_id=user.id)

    if date:
        order.created_at = date
        order.save()

    tickets_to_create = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )
        for ticket in tickets
    ]

    for ticket in tickets_to_create:
        ticket.full_clean()

    Ticket.objects.bulk_create(tickets_to_create)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
