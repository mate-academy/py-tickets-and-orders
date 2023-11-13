from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        order = Order(user=user)
        order.save()
        if date:
            order.created_at = date
        order.save()
        for ticket in tickets:
            ticket = Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            ticket.save()


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    order_set = Order.objects.all()
    if username:
        order_set = order_set.filter(user__username=username)
    return order_set
