from django.contrib.auth import get_user_model

from django.db import transaction

from db.models import Ticket, Order

from datetime import datetime


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        if date:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order = Order.objects.create(user=user, created_at=created_at)
        else:
            order = Order.objects.create(user=user)

        for ticket in tickets:
            new_ticket = Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            new_ticket.save()

    return order

def get_orders(username: str = None) -> list[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()