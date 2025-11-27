from django.db import transaction
from datetime import datetime
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model

User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)
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
    return order


@transaction.atomic
def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
