from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet


from db.models import Order, Ticket


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            created_at = parse_datetime(date)
            Order.objects.filter(id=order.id).update(created_at=created_at)

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    user_model = get_user_model()
    if username:
        user = user_model.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
