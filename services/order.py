import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        if date is not None:
            order = Order.objects.create(
                user=user,
                created_at=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
            )
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
            )

    return order


def get_orders(
        username: str = None,
) -> QuerySet:
    qs = Order.objects.all().select_related("user")
    if username:
        return qs.filter(user__username=username)
    return qs
