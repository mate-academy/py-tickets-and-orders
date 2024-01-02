from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.user import get_user_by_username


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    user = get_user_by_username(username)
    order = Order.objects.create(user=user)
    if date:
        _date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.id).update(created_at=_date)
    for ticket_dict in tickets:
        ticket_dict["movie_session_id"] = ticket_dict["movie_session"]
        del ticket_dict["movie_session"]
        Ticket.objects.create(order=order, **ticket_dict)


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        user = get_user_by_username(username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
