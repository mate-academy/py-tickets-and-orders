from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list[dict],
                 movie_session: int,
                 username: str,
                 date: str = None) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order.date = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order_id=order.id,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
    return order


def get_orders(username: str) -> QuerySet[Order]:
    if username:
        Order.objects.filter(user__username=username)
    Order.objects.all()
