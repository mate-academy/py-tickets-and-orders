from datetime import datetime
from typing import List, Dict, Union
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Union[str, datetime] = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )

    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
