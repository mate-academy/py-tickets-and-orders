from django.db import transaction

from db.models import Ticket, User, Order, MovieSession
from django.db.models import DateTimeField, QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: DateTimeField = None
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    Ticket.objects.bulk_create([
        Ticket(
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets
    ])


def get_orders(username: str = None) -> QuerySet:
    if username:

        return Order.objects.filter(user__username=username)

    return Order.objects.all().order_by("-user__username")
