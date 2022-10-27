from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    new_user = get_user_model().objects.get(username=username)
    new_order = Order.objects.create(user=new_user)

    if date:
        new_order.created_at = date
        new_order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=new_order
        )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(
            user__username=username
        ).order_by("-user")
    return Order.objects.order_by("-user")
