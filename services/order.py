import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from services.user import get_user_by_username


def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> None:
    user = get_user_by_username(username)
    with transaction.atomic():
        if date:
            date_from_str = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(created_at=date_from_str, user=user)
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
