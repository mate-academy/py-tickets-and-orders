from django.contrib.auth import get_user_model

from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(created_at=date, user=user)

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")

        order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            ).save()

        return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
