from datetime import datetime

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(tickets: list,
                 username: str,
                 date: datetime = None,
                 ) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=order.id,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> Order:
    order = Order.objects.all()
    if username:
        user = User.objects.get(username=username)
        order = Order.objects.filter(user_id=user.id)
    return order
