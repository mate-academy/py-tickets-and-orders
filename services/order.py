from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> QuerySet:
    user = User.objects.get(username=username)
    order = Order.objects.create(
        user=user,
    )
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        row = ticket["row"]
        seat = ticket["seat"]
        movie_session = ticket["movie_session"]
        Ticket.objects.create(
            movie_session_id=movie_session,
            row=row,
            seat=seat,
            order=order,
        )
    return Order.objects.all()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
