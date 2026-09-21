import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.datetime = None,
) -> Order:

    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    tickets_to_create = []

    for ticket_dict in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket_dict["movie_session"],
            row=ticket_dict["row"],
            seat=ticket_dict["seat"]
        )

        ticket.full_clean()
        tickets_to_create.append(ticket)

    Ticket.objects.bulk_create(tickets_to_create)

    return order


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
