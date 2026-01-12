from django.db import transaction
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
User = get_user_model()


def create_order(
    tickets: list,
    username: str,
    date: str = None,
) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = parse_datetime(date)
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order=order,
            )
        return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
