from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

import init_django_orm  # noqa
from db.models import Order, Ticket
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(
            username=username
        )
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()
        Ticket.objects.bulk_create(
            [
                Ticket(
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=get_movie_session_by_id(
                        ticket["movie_session"]
                    )
                ) for ticket in tickets
            ]
        )

    return order


def get_orders(
        username: str = None
) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
