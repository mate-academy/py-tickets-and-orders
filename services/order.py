from django.db.models import QuerySet
from typing import Optional
from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


User = get_user_model()


@transaction.atomic
def create_order(
        tickets: list,
        username: str,
        date: Optional[str] = None
) -> Order:
    user = User.objects.get(username=username)
    order_data = {"user": user}
    if date:
        order_data["created_at"] = datetime.fromisoformat(date)

    order = Order.objects.create(**order_data)

    for ticket in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"]
        )
        ticket.full_clean()  # проверка row и seat
        ticket.save()

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
