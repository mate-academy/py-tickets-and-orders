from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> \
        None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            movie_session_id=ticket["movie_session"],
            seat=ticket["seat"],
            row=ticket["row"]
        )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders
