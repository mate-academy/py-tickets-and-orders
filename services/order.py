from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from typing import Optional
from django.contrib.auth import get_user_model


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str]
) -> Order:
    user = User.objects.get(username=username)
    if date:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)
    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        user = User.objects.get(username=username)
        queryset = queryset.filter(user=user)

    return queryset
