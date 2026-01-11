from typing import List, Dict, Optional
from django.utils.timezone import make_aware
from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, MovieSession, User


def create_order(
    tickets: List[Dict[str, int]], username: str, date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError(f"User with username '{username}' does not exist")

        order = Order.objects.create(user=user)

        if date:
            try:
                order.created_at = make_aware(
                    datetime.strptime(date, "%Y-%m-%d %H:%M")
                )
                order.save()
            except ValueError:
                raise ValueError(
                    "Invalid date format, expected 'YYYY-MM-DD HH:MM'"
                )

        ticket_objects = []
        for ticket in tickets:
            try:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ValueError(
                    f"Movie session {ticket["movie_session"]} does not exist"
                )

            ticket_objects.append(
                Ticket(
                    order=order,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session=movie_session,
                )
            )

        Ticket.objects.bulk_create(ticket_objects)
        return order


def get_orders(username: Optional[str] = None) -> List[int]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    orders = orders.order_by("-created_at")

    orders_values = orders.values_list("id", flat=True)

    return list(orders_values)
