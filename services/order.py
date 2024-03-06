from typing import Callable, Any

from datetime import date
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


def transactional_function(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper


@transactional_function
def create_order(
        tickets: list[dict],
        username: str,
        date: date | None = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
