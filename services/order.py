import datetime

from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime | None = None
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session_id=ticket.get("movie_session")
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
