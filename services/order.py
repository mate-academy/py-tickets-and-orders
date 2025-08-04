from dateutil.parser import parse
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)
        if date is not None:
            order.created_at = parse(date)
            order.save()

        for ticket_info in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_info.get("movie_session"),
                order=order,
                row=ticket_info.get("row"),
                seat=ticket_info.get("seat"),
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
