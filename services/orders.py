from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from django.db import transaction
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str, date: str | None = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = parse_datetime(date)
        Order.objects.filter(id=order.id).update(created_at=order.created_at)
        order.refresh_from_db()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
