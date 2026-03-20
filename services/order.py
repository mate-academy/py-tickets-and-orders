from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)

    order_params = {"user": user}
    if date:
        order_params["created_at"] = date

    order = Order.objects.create(**order_params)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order, Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
