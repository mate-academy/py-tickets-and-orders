from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from db.models import User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
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


def get_orders(username: str = None) -> QuerySet[str]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
