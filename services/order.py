from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket.get("movie_session"),
                row=ticket.get("row"),
                seat=ticket.get("seat"),
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        with transaction.atomic():
            order = Order.objects.filter(
                user=get_user_model().objects.get(username=username)
            )
            return order
    else:
        order = Order.objects.all()
        return order
