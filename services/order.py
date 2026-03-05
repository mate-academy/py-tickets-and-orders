from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:

    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            seat=ticket["seat"],
            row=ticket["row"]
        )

    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:

    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
