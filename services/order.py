from typing import Optional, List, Dict

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Order, Ticket, MovieSession


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise User.DoesNotExist("Username not found")
    order_created_at = None
    if date:
        order_created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    order = Order.objects.create(
        user=user,
        created_at=order_created_at
    )
    for _ in tickets:
        movie_session = MovieSession.objects.get(id=_["movie_session"])

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=_["row"],
            seat=_["seat"]
        )
    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    return Order.objects.filter(user__username=username)\
        if username else Order.objects.all()
