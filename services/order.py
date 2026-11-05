from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet, DateTimeField

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list[dict[str, int]],
                 username: str,
                 date: DateTimeField = None) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
