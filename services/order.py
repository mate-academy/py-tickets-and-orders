from django.db.models import QuerySet

from db.models import Ticket, Order
from django.contrib.auth import get_user_model
from django.db import transaction


def create_order(
        tickets: list,
        username: str,
        date: str = None

) -> None:
    with transaction.atomic():

        new_order = Order.objects.create(
            user=get_user_model().objects.get(username=username)
        )

        if date:
            Order.objects.filter(pk=new_order.id).update(created_at=date)

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=new_order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
