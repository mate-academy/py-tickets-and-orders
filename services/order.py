from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime

from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list,
                 username: str,
                 date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        parsed_date = parse_datetime(date)
        if not parsed_date:
            raise ValueError(
                "Invalid date format."
            )
        Order.objects.filter(id=order.id).update(created_at=parsed_date)

    for ticket_data in tickets:
        ticket = Ticket(
            order=order,
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
        ticket.full_clean()
        ticket.save()
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset.order_by("-created_at")
