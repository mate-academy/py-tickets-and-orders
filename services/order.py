from typing import Optional, List, Dict

from django.contrib.auth import get_user_model

from django.db import transaction

from django.db.models import QuerySet

from django.utils import timezone

from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None,
) -> None:
    with transaction.atomic():
        if date:
            created_at = parse_datetime(date)
        else:
            created_at = timezone.now()

        user_model = get_user_model()
        user = user_model.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = created_at
            order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            )


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    order_query = Order.objects.all()
    if username:
        order_query = order_query.filter(user__username=username)
    return order_query
