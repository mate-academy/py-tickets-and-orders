import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | datetime.datetime = None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        parsed_date = (
            datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            if isinstance(date, str)
            else date
        )
        Order.objects.filter(id=order.id).update(created_at=parsed_date)
        order.refresh_from_db()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )
    return order


def get_orders(
    username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
