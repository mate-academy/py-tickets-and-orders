from django.db import transaction
from db.models import Order, Ticket, User
from django.utils.dateparse import parse_datetime


@transaction.atomic
def create_order(
    tickets: Order,
    username: str = None,
    date: str = None
) -> Order:
    user = None
    if username:
        user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = parse_datetime(date)
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str = None) -> Order:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
