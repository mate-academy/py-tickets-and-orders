from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.db import transaction
import init_django_orm  # noqa: F401

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order)

    return order


def get_orders(username: str = None) -> QuerySet(Order):
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
