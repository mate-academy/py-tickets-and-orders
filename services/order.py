from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date

    order.save()

    tickets_obj = [
        Ticket(
            order=order,
            movie_session=MovieSession.objects.filter(
                pk=ticket["movie_session"]
            ).first(),
            row=ticket["row"],
            seat=ticket["seat"]
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(tickets_obj)

    return order


@transaction.atomic
def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = Order.objects.filter(user__username=username)

    return orders
