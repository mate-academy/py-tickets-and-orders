from django.db import transaction
from db.models import Order, Ticket
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model


@transaction.atomic()
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None) -> QuerySet(Order):
    orders = Order.objects.select_related("user")
    if username:
        orders = orders.filter(user__username=username)
    return orders
