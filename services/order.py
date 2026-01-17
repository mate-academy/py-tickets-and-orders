from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from services.movie_session import get_movie_session_by_id
from db.models import Order, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: datetime = None,
) -> Order:
    user_model = get_user_model()
    user, _ = user_model.objects.get_or_create(
        username=username,
        defaults={"password": "123"}
    )

    order = Order.objects.create(
        user=user,
    )

    if date:
        order.created_at = date
        order.save()

    tickets_data = [
        Ticket(
            movie_session=get_movie_session_by_id(
                ticket["movie_session"]
            ),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(tickets_data)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
