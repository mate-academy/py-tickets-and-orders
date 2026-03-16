from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        dt_object = datetime.fromisoformat(date)
        Order.objects.filter(pk=order.pk).update(created_at=dt_object)
        order.refresh_from_db()

    tickets = [
        Ticket(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        ) for ticket in tickets
    ]
    for ticket in tickets:
        ticket.save()

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.select_related(
            "user").filter(user__username=username)
    return queryset
