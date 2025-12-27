from datetime import datetime
import logging
from typing import TypedDict

from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket, User


logger = logging.getLogger(__name__)


class OrderFields(TypedDict, total=False):
    user: User
    created_at: datetime


class TicketData(TypedDict):
    movie_session: int
    row: int
    seat: int


def parse_date_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M")


@transaction.atomic
def create_order(
    tickets: list[TicketData],
    username: str,
    date: str | datetime | None = None,
) -> Order:
    user = get_user_model().objects.get(username=username)

    order_fields: OrderFields = {
        "user": user,
    }

    if date is not None:
        if isinstance(date, str):
            date = parse_date_str(date)
        order_fields["created_at"] = date

    order = Order.objects.create(**order_fields)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    if settings.DEBUG:
        logger.info(
            f"Order {order.id} created for user {username!r} "
            f"with {len(tickets)} ticket(s)"
        )

    return order


def get_orders(
    username: str | None = None,
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
