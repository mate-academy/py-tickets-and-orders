from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime

from db.models import Ticket, User, Order


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None) -> Order:

    user, _ = User.objects.get_or_create(username=username)

    order = Order.objects.create(user=user)
    if date is not None:
        try:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

    order.save(update_fields=["created_at"])

    tickets_to_base = []
    for ticket in tickets:
        ticket_obj = Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )
        ticket_obj.full_clean()
        tickets_to_base.append(ticket_obj)

    Ticket.objects.bulk_create(tickets_to_base)

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
