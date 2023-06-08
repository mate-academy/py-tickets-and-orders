from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> Order | None:
    with transaction.atomic():
        order = Order.objects.create(
            user=get_user_model().objects.get(username=username),
        )

        if date is not None:
            Order.objects.filter(id=order.id).update(created_at=date)

        Ticket.objects.bulk_create(
            [
                Ticket(
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=MovieSession.objects.get(
                        id=ticket["movie_session"]),
                    order=order,
                )
                for ticket in tickets
            ]
        )

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
