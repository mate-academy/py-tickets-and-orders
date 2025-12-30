from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id
from services.user import get_user_by_username


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> None:
    order = Order(user=get_user_by_username(username))
    order.save()
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session=get_movie_session_by_id(
                ticket.get("movie_session")
            ),
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders_query = Order.objects.all()
    if username:
        orders_query = orders_query.filter(user__username=username)
    return orders_query
