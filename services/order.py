from datetime import datetime

from django.db.models import QuerySet
from db.models import Order, Ticket, User
from django.db import transaction


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None,
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=created_at)
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
        )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
