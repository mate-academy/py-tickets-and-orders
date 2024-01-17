from django.db import transaction
from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.all()
        order_create = order.create(user__username=username)
        if date:
            order_create.created_at = order.date
            order_create.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order_create,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
