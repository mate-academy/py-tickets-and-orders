from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession


def create_order(
    tickets: list[dict],
    username: str,
    date: datetime | str = None
) -> Order:

    user = get_user_model().objects.get(username=username)

    @transaction.atomic
    def order_creating() -> Order:
        order = Order(user=user)
        order.save()

        ticket_objects = [Ticket(
            movie_session=MovieSession.objects.get(pk=ticket["movie_session"]),
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        ) for ticket in tickets]

        Ticket.objects.bulk_create(ticket_objects)
        return order

    order = order_creating()
    if type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    if date:
        order.created_at = date
        order.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
