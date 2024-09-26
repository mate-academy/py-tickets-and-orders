from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from django.db import transaction


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> None:
    new_order = Order.objects.create(
        user_id=get_user_model().objects.get(username=username).id
    )
    if date:
        new_order.created_at = date
    new_order.save()
    Ticket.objects.bulk_create(
        [
            Ticket(
                order=new_order,
                movie_session=MovieSession.objects.get(
                    id=tickets[i]["movie_session"]
                ),
                row=tickets[i]["row"],
                seat=tickets[i]["seat"]
            ) for i in range(len(tickets))
        ]
    )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return orders
