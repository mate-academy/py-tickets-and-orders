from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order
from db.models import Ticket
from datetime import datetime


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order:
    user = get_user_model()
    user = user.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
