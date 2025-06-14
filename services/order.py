import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import User, Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    created_at = datetime.datetime.strptime(
        date, "%Y-%m-%d %H:%M"
    ) if date else datetime.datetime.now()
    order = Order.objects.create(user=user, created_at=created_at)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
