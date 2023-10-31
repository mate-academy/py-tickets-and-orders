from django.db import transaction
from db.models import Ticket, Order
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import QuerySet


def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data.get("row"),
                seat=ticket_data.get("seat"),
                movie_session_id=ticket_data.get("movie_session"),
                order=order,
            )
        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
