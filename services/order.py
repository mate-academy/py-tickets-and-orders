from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket
from services.user import get_user


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = get_user(user_id=User.objects.get(username=username).id)

        order = Order.objects.create(
            user=user
        )
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.order_by("-user")
