from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str | None = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        created_at = datetime.strptime(
            date, "%Y-%m-%d %H:%M"
        )

        Order.objects.filter(id=order.id).update(
            created_at=created_at
        )

        order.created_at = created_at

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
