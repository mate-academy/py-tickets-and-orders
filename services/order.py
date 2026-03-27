from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:

    order = Order.objects.create(
        user=User.objects.get(username=username))

    if date is not None:
        order.created_at = date
        order.save()

    for ticket in tickets:
        order.tickets.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session_id=ticket.get("movie_session"),
            order=order.id)


def get_orders(username: str = None) -> QuerySet:
    query = Order.objects.all()
    if username is not None:
        query = query.filter(user__username=username)
    return query
