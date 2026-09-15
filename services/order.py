from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        Order.objects.filter(id=order.id).update(created_at=date)
    tickets_list = [
        Ticket(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
        for ticket in tickets
    ]
    for ticket in tickets_list:
        ticket.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
