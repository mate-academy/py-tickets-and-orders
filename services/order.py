from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    new_order = Order.objects.create(
        user=get_user_model().objects.get(username=username),
        created_at=date
    )

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order=new_order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
