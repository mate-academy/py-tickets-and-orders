from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import User, Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    if date:
        date = datetime.fromisoformat(date)
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"]
            )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
