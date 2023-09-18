from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict], username: str, date: str | None = None
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
