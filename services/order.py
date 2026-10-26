from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from datetime import datetime
from db.models import Order, Ticket
from django.db import transaction


@transaction.atomic
def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    user_instance = get_user_model().objects.get(username=username)
    order_kwargs = {"user": user_instance}
    if date:
        order_kwargs["created_at"] = date
    order = Order.objects.create(**order_kwargs)
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
