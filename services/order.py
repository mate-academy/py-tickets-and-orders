from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    with transaction.atomic():
        if username is not None:
            return Order.objects.filter(user__username=username)
    return Order.objects.all()
