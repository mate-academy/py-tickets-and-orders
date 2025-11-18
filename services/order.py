from datetime import datetime
from django.db import transaction

from db.models import Order, Ticket, User
from django.db.models import QuerySet


def create_order(tickets: list, username: str,
                 date: str | None = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            created_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
            Order.objects.filter(id=order.id).update(created_at=created_time)

            order.refresh_from_db()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                order=order,
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)

    return queryset


def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)
