from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from db.models import Order, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: str | None = None,
) -> Order:
    with transaction.atomic():
        order = Order(
            user=get_user_model().objects.get(username=username),
        )
        order.save()
        if date:
            # save again to override `auto_now_add`
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )
    return order


def get_orders(username: str | None = None) -> QuerySet:
    query = Order.objects.all()

    if username:
        query = query.filter(user__username=username)

    return query
