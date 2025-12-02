from django.contrib.auth import get_user_model
from django.db import transaction
import datetime
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str, date: str = None
) -> Order:

    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=dt)
        order.created_at = dt

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:

    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
