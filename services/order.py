from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = datetime.now()
    order = Order.objects.create(
        user=user,
        created_at=created_at,
    )

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.select_related("user").prefetch_related("tickets")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
