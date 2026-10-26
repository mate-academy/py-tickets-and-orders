from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from datetime import datetime


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(pk=order.pk).update(created_at=order.created_at)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    user_model = get_user_model()
    if username:
        user = user_model.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
