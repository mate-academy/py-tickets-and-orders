from django.db import transaction
from db.models import Order, Ticket
from django.contrib.auth import get_user_model
from django.db.models import QuerySet


def create_order(
    tickets: list,
    username: str,
    date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user, created_at=date)
        if date:
            order.created_at = date
            order.save()

        for data in tickets:
            Ticket.objects.create(
                movie_session_id=data["movie_session"],
                order=order,
                row=data["row"],
                seat=data["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
