from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order.created_at = datetime.strptime(
            date,
            "%Y-%m-%d %H:%M"
        )

    order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            movie_session=get_movie_session_by_id(
                ticket_data.get("movie_session")
            ),
            row=ticket_data.get("row"),
            seat=ticket_data.get("seat")
        )


def get_orders(
        username: Optional[str] = None
) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
