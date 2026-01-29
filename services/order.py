from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order
from django.contrib.auth import get_user_model


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    current_user = get_user_model()
    user = current_user.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        Order.objects.filter(id=order.id).update(created_at=date)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
