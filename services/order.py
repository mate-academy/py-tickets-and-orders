from datetime import datetime

from django.db.models import QuerySet

from db.models import Order, Ticket
from django.db import transaction
from django.contrib.auth import get_user_model


User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders_query = Order.objects.all()

    if username:
        orders_query = Order.objects.filter(user__username=username)

    return orders_query
