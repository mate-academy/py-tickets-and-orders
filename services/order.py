from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> None:

    user = get_user_model().objects.get(username=username)

    if date is not None:
        order = Order.objects.create(user=user, created_at=date)
    else:
        order = Order.objects.create(user=user)

    for ticket_data in tickets:
        ticket = Ticket.objects.create(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.full_clean()
        ticket.save()


def get_orders(username: str = None) -> QuerySet[Order] | None:
    if username:
        user_id = get_user_model().objects.get(username=username)
        return Order.objects.filter(user_id=user_id)
    return Order.objects.all()
