from typing import List
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(
        tickets: List[dict],
        username: str,
        date: str | None = None
) -> Order:
    # Використовуємо get_user_model() для надійності
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        # КРИТИЧНО: для полів з auto_now_add дату треба ставити ТАК:
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        # Фільтруємо через зв'язок, щоб не шукати користувача окремо
        queryset = queryset.filter(user__username=username)
    return queryset
