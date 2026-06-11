from django.db.models import QuerySet
from datetime import datetime
from django.db import transaction

from db.models import Ticket, User, Order


@transaction.atomic
def create_order(
    tickets: list,
    username: str,
    date: datetime = None,
) -> Order:
    user = User.objects.get(username=username)
    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = datetime.now()
    order = Order.objects.create(
        user=user,
        created_at=created_at
    )
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )
    return order


def get_orders(
    username: str = None,
) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
