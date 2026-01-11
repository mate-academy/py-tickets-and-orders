from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        row = ticket.get("row")
        seat = ticket.get("seat")
        movie_session_id = ticket.get("movie_session")
        Ticket.objects.create(
            row=row,
            seat=seat,
            movie_session_id=movie_session_id,
            order=order
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
