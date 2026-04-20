import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: str | None = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        parsed_date = datetime.datetime.strptime(
            date, "%Y-%m-%d %H:%M"
        )

        order.created_at = parsed_date
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order,
        )

    return order


def get_orders(
    username: str | None = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
