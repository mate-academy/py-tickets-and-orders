import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = date
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )
        order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    query_set = Order.objects.all()
    if username:
        query_set = query_set.filter(user__username=username)
    return query_set
