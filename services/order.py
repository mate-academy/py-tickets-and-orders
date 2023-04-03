from typing import List

import init_django_orm  # noqa: F401 щоб імпортувати,
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(
    tickets: List[dict],
    username: str,
    date: str = None,
) -> Ticket:

    with transaction.atomic():
        find_user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user_id=find_user.id)

        if date:
            order.created_at = date
            order.save()
        for ticket_data in tickets:
            new_ticket = Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order_id=order.id
            )

    return new_ticket


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        find_user = get_user_model().objects.get(username=username)
        queryset = queryset.filter(user_id=find_user.id)

    return queryset
