from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date

        Ticket.objects.bulk_create([
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                order_id=order.id,
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            )
            for ticket in tickets])

    order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    order = Order.objects.order_by("-user")

    if username:
        order = Order.objects.filter(user__username=username)

    return order
