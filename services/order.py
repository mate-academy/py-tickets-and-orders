import datetime
from typing import Optional, List, Dict

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from db.models import Order, Ticket

UserModel = get_user_model()


def _parse_date(date_str: str) -> datetime.datetime:
    for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
    ):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return datetime.datetime.fromisoformat(date_str)


@transaction.atomic
def create_order(
        tickets: List[Dict],
        username: str,
        date: Optional[str] = None,
) -> Order:
    try:
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        raise ObjectDoesNotExist(
            f"User with username={username} does not exist"
        )

    order = Order.objects.create(user=user)
    if date:
        order.created_at = _parse_date(date)
        order.save(update_fields=["created_at"])

    for ticket_data in tickets:
        ticket_data["movie_session_id"] = ticket_data.pop("movie_session")
        Ticket.objects.create(order=order, **ticket_data)

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return (
            Order.objects.filter(user__username=username)
            .order_by("-created_at")
        )
    return Order.objects.all().order_by("-created_at")
