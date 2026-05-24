from django.db.models import QuerySet
from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: str | None = None) -> Order:
    user = User.objects.get(username=username)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
