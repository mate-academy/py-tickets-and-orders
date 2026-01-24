from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.utils.dateparse import parse_datetime
from typing import Any


def create_order(tickets: list[dict], username: str,
                 date: Any = None) -> Order:
    user = get_user_model().objects.get(username=username)

    with transaction.atomic():
        if date:
            parsed_date = parse_datetime(date)
            if parsed_date:
                order = Order(user=user, created_at=parsed_date)
                order.save()
            else:
                raise ValueError("Invalid date format")
        else:
            order = Order.objects.create(user=user)

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]),
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
        return order


def get_orders(username: Any = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
