from django.db.models import QuerySet

from db.models import Ticket, Order, User
from django.db import transaction


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket.get("movie_session"),
                order_id=order.id,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )
        return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        user = User.objects.get(username=username)
        queryset = queryset.filter(user=user)

    return queryset
