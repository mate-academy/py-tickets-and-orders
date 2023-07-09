from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.user import get_user_by_username


def create_preorder(username: str, date: str | None) -> int:
    order = Order.objects.create(
        user=get_user_by_username(username)
    )
    if date:
        order.created_at = date
    order.save()
    return order.id


@transaction.atomic()
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> None:
    order = create_preorder(username, date)

    pretickets = [
        Ticket(
            movie_session_id=ticket.get("movie_session"),
            order_id=order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
        for ticket in tickets
    ]

    # model.save() does not work in bulk-operations
    for preticket in pretickets:
        preticket.clean()

    Ticket.objects.bulk_create(pretickets)


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
