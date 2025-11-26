from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order(
            user=user,
        )

        order.full_clean()
        order.save()

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        tickets_objs = [
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        for ticket in tickets_objs:
            ticket.full_clean()  # проверка перед сохранением
        Ticket.objects.bulk_create(tickets_objs)


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
