from django.db import transaction
from db.models import Order, Ticket, MovieSession, User
from django.core.exceptions import ObjectDoesNotExist
from typing import Optional


def create_order(tickets: list, username: str,
                 date: Optional[str] = None) -> None:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    pk=ticket_data["movie_session"]),
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
    return order


def get_orders(username: str = None) -> None:
    if username:
        return Order.objects.filter(
            user__username=username).order_by("-created_at")
    return Order.objects.all().order_by("-created_at")
