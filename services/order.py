from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )

    if date:
        order.created_at = date

    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> QuerySet:
    query = Order.objects.all()

    if username:
        query = query.filter(user__username=username)

    return query
